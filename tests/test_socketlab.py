import concurrent.futures
import socket
import threading
import unittest
from socketlab.core import Lab, exact, recv_frame, send_frame, PAYLOAD

class SocketTests(unittest.TestCase):
    def setUp(self): self.lab=Lab(0,0,0)
    def tearDown(self): self.lab.stop()
    def test_all_scenarios(self):
        expected={"baseline":["HEALTHY"],"tcp_off":["TCP_UNAVAILABLE"],"delay":["RESPONSE_DELAY"],"udp_loss":["UDP_LOSS"],"dns_wrong":["DNS_MISMATCH"],"corrupt":["FILE_CORRUPTED"],"combined":["DNS_MISMATCH","TCP_UNAVAILABLE"]}
        for mode, findings in expected.items():
            with self.subTest(mode=mode):
                result=self.lab.run(mode)
                self.assertEqual(result["findings"],findings)
                if mode == "baseline":
                    self.assertTrue(all(x["integrity"] for x in result["evidence"]["concurrent"]))
                    self.assertEqual(result["evidence"]["direct_tcp"]["bytes"],len(PAYLOAD))
                if mode == "udp_loss": self.assertEqual(result["evidence"]["udp"]["loss_percent"],50)
        self.assertEqual(self.lab.run()["findings"],["HEALTHY"])
    def test_duplicate_udp_listener_rejected(self):
        from socketlab.core import UDPServer, UDPHandler
        first=UDPServer(("127.0.0.1",0),UDPHandler)
        try:
            with self.assertRaises(OSError):
                second=UDPServer(first.server_address,UDPHandler)
                second.server_close()
        finally: first.server_close()

    def test_fragmented_frame(self):
        a,b=socket.socketpair()
        with a,b:
            a.sendall(b"\0\0"); a.sendall(b"\0\5he"); a.sendall(b"llo")
            self.assertEqual(recv_frame(b),b"hello")
    def test_early_close(self):
        a,b=socket.socketpair(); a.sendall(b"\0\0\0\5hi"); a.close()
        with b: self.assertRaises(ConnectionError,recv_frame,b)
    def test_size_limit(self):
        a,b=socket.socketpair()
        with a,b:
            a.sendall(b"\xff\xff\xff\xff")
            self.assertRaises(ValueError,recv_frame,b)
    def test_concurrent_clients(self):
        self.lab.configure("baseline")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            self.assertTrue(all(r["integrity"] for r in pool.map(lambda _:self.lab.download(),range(10))))

if __name__ == "__main__": unittest.main()
