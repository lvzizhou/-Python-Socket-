"""Real loopback Socket services, framed TCP protocol and measured probes."""
import concurrent.futures
import hashlib
import json
import socket
import socketserver
import struct
import threading
import time
import uuid
from datetime import datetime, timezone

PAYLOAD = bytes(range(256)) * 4096
SCENARIOS = {
    "baseline": "正常通信", "tcp_off": "TCP 服务停止", "delay": "应用响应延迟",
    "udp_loss": "UDP 应用层丢包", "dns_wrong": "DNS 错误解析",
    "corrupt": "文件内容损坏", "combined": "错误解析与 TCP 停服叠加",
}

def exact(sock, size):
    chunks = bytearray()
    while len(chunks) < size:
        block = sock.recv(size-len(chunks))
        if not block:
            raise ConnectionError("连接提前关闭")
        chunks.extend(block)
    return bytes(chunks)

def send_frame(sock, data):
    sock.sendall(struct.pack("!I", len(data)) + data)

def recv_frame(sock, limit=2*1024*1024):
    size = struct.unpack("!I", exact(sock, 4))[0]
    if size > limit:
        raise ValueError("报文超过长度上限")
    return exact(sock, size)

class TCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

class UDPServer(socketserver.ThreadingUDPServer):
    allow_reuse_address = True
    daemon_threads = True

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(3)
        try:
            request = json.loads(recv_frame(self.request))
            if request.get("op") != "download":
                send_frame(self.request, b'{"error":"unknown operation"}')
                return
            if self.server.mode == "delay":
                time.sleep(0.35)
            data = PAYLOAD
            if self.server.mode == "corrupt":
                data = b"X" + data[1:]
            meta = {"size": len(data), "sha256": hashlib.sha256(PAYLOAD).hexdigest()}
            send_frame(self.request, json.dumps(meta).encode())
            send_frame(self.request, data)
        except (OSError, ValueError, ConnectionError):
            return

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        try:
            msg = json.loads(data)
            # Deterministic, reproducible application-level discard: odd sequences.
            if self.server.mode == "udp_loss" and msg["seq"] % 2:
                return
            sock.sendto(data, self.client_address)
        except (ValueError, KeyError, OSError):
            pass

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        if len(data) < 17 or struct.unpack("!H", data[4:6])[0] != 1:
            return
        pos, labels = 12, []
        while pos < len(data):
            size = data[pos]; pos += 1
            if not size: break
            if size > 63 or pos+size > len(data): return
            labels.append(data[pos:pos+size]); pos += size
        if pos+4 != len(data): return
        known = b".".join(labels).lower() == b"service.lab.test" and data[pos:pos+4] == b"\x00\x01\x00\x01"
        ip = "127.0.0.2" if self.server.mode in ("dns_wrong", "combined") else "127.0.0.1"
        header = data[:2] + struct.pack("!HHHHH", 0x8400 if known else 0x8403, 1, int(known), 0, 0)
        answer = struct.pack("!HHHIH", 0xc00c, 1, 1, 0, 4) + socket.inet_aton(ip)
        sock.sendto(header+data[12:]+(answer if known else b""), self.client_address)

class Lab:
    def __init__(self, tcp=19090, udp=19091, dns=15353):
        self.ports = {"tcp": tcp, "udp": udp, "dns": dns}
        self.servers = []
        self.mode = None
        self.lock = threading.RLock()

    def stop(self):
        for server, thread in self.servers:
            server.shutdown(); server.server_close(); thread.join(timeout=2)
        self.servers = []

    def configure(self, mode):
        if mode not in SCENARIOS: raise ValueError("未知场景")
        self.stop()
        try:
            for key, cls, handler in [("tcp", TCPServer, TCPHandler), ("udp", UDPServer, UDPHandler), ("dns", UDPServer, DNSHandler)]:
                if key == "tcp" and mode in ("tcp_off", "combined"): continue
                server = cls(("127.0.0.1", self.ports[key]), handler)
                self.ports[key] = server.server_address[1]
                server.mode = mode
                thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": .02}, daemon=True)
                self.servers.append((server, thread)); thread.start()
            self.mode = mode
        except Exception:
            self.stop(); raise

    def resolve(self):
        ident = uuid.uuid4().int & 65535
        query = struct.pack("!HHHHHH", ident, 0x100, 1, 0, 0, 0) + b"\x07service\x03lab\x04test\x00\x00\x01\x00\x01"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(.5); sock.connect(("127.0.0.1", self.ports["dns"]))
            sock.send(query); data = sock.recv(512)
        if len(data) < 16 or data[:2] != query[:2] or data[6:8] != b"\x00\x01":
            raise ValueError("DNS 响应无效")
        return socket.inet_ntoa(data[-4:])

    def download(self, host="127.0.0.1"):
        start = time.perf_counter()
        try:
            with socket.create_connection((host, self.ports["tcp"]), timeout=.8) as sock:
                send_frame(sock, b'{"op":"download"}')
                meta = json.loads(recv_frame(sock)); data = recv_frame(sock)
            elapsed = time.perf_counter()-start
            valid = len(data) == meta["size"] and hashlib.sha256(data).hexdigest() == meta["sha256"]
            return {"ok": True, "host": host, "bytes": len(data), "ms": round(elapsed*1000,2), "mbps": round(len(data)*8/elapsed/1e6,2), "integrity": valid}
        except (OSError, ValueError, KeyError, ConnectionError) as exc:
            return {"ok": False, "host": host, "ms": round((time.perf_counter()-start)*1000,2), "error": type(exc).__name__, "detail": str(exc)}

    def udp_probe(self, count=8):
        received, rtts = 0, []
        token = uuid.uuid4().hex
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(.12); sock.connect(("127.0.0.1", self.ports["udp"]))
            for seq in range(count):
                message = json.dumps({"token": token, "seq": seq}).encode(); start=time.perf_counter()
                sock.send(message)
                try:
                    if sock.recv(2048) == message:
                        received += 1; rtts.append((time.perf_counter()-start)*1000)
                except socket.timeout: pass
        return {"sent": count, "received": received, "loss_percent": round((count-received)*100/count,1), "rtt_ms": round(sum(rtts)/len(rtts),3) if rtts else None}

    def run(self, mode="baseline", clients=3):
        with self.lock:
            self.configure(mode)
            evidence, findings = {}, []
            try: evidence["dns"] = {"ok": True, "address": self.resolve()}
            except (OSError, ValueError) as exc: evidence["dns"] = {"ok": False, "error": str(exc)}
            evidence["direct_tcp"] = self.download()
            evidence["domain_tcp"] = self.download(evidence["dns"]["address"]) if evidence["dns"]["ok"] else {"ok": False}
            evidence["udp"] = self.udp_probe()
            with concurrent.futures.ThreadPoolExecutor(max_workers=clients) as pool:
                evidence["concurrent"] = list(pool.map(lambda _: self.download(), range(clients)))
            # Diagnosis uses observed evidence only; the injected mode is not consulted.
            if not evidence["dns"]["ok"]: findings.append("DNS_NO_RESPONSE")
            elif evidence["dns"]["address"] != "127.0.0.1": findings.append("DNS_MISMATCH")
            tcp = evidence["direct_tcp"]
            if not tcp["ok"]: findings.append("TCP_UNAVAILABLE")
            elif not tcp["integrity"]: findings.append("FILE_CORRUPTED")
            elif tcp["ms"] > 250: findings.append("RESPONSE_DELAY")
            if evidence["udp"]["loss_percent"] > 0: findings.append("UDP_LOSS")
            return {"id": uuid.uuid4().hex[:12], "time": datetime.now(timezone.utc).isoformat(), "scenario": mode, "ports": dict(self.ports), "findings": findings or ["HEALTHY"], "evidence": evidence}
