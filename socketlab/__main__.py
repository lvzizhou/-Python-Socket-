import argparse
import json
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from .core import Lab, SCENARIOS

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Python Socket 网络实验平台")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    lab = Lab()
    results = ROOT / "results"; results.mkdir(exist_ok=True)
    if args.batch:
        try:
            runs = [lab.run(mode) for mode in SCENARIOS]
            (results/"batch.json").write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps([{ "scenario": r["scenario"], "findings": r["findings"]} for r in runs], ensure_ascii=False, indent=2))
        finally: lab.stop()
        return
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw): super().__init__(*a, directory=str(ROOT/"docs"), **kw)
        def reply(self, status, obj):
            data=json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
        def do_GET(self):
            if urlsplit(self.path).path == "/api/status":
                self.reply(200, {"live": True, "scenarios": SCENARIOS}); return
            super().do_GET()
        def do_POST(self):
            # Local UI only: reject cross-origin browser requests.
            if self.headers.get("Origin") not in (None, f"http://127.0.0.1:{args.port}", f"http://localhost:{args.port}"):
                self.reply(403, {"error": "不接受跨站请求"}); return
            if self.path != "/api/run": self.reply(404, {"error": "接口不存在"}); return
            try:
                size=int(self.headers.get("Content-Length", "0"))
                if size < 1 or size > 2048: raise ValueError("请求长度无效")
                request=json.loads(self.rfile.read(size))
                clients=int(request.get("clients", 3))
                if not 1 <= clients <= 10: raise ValueError("并发数应在 1 到 10 之间")
                if not lab.lock.acquire(blocking=False):
                    self.reply(409, {"error": "已有实验正在运行"}); return
                try: record=lab.run(request.get("scenario", "baseline"), clients)
                finally: lab.lock.release()
                (results/(record["id"]+".json")).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
                self.reply(200, record)
            except (ValueError, TypeError) as exc: self.reply(400, {"error": str(exc)})
            except OSError as exc: self.reply(500, {"error": "端口占用或网络错误："+str(exc)})
    server=ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"打开 http://127.0.0.1:{args.port} ，按 Ctrl+C 退出")
    if not args.no_browser: threading.Timer(.5, lambda: webbrowser.open(f"http://127.0.0.1:{args.port}")).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close(); lab.stop()

if __name__ == "__main__": main()
