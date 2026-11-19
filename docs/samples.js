window.SAMPLES = [
  {
    "id": "7f49529ccf60",
    "time": "2026-11-19T10:28:58.480331+00:00",
    "scenario": "baseline",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "HEALTHY"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.1"
      },
      "direct_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 3.77,
        "mbps": 2226.45,
        "integrity": true
      },
      "domain_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 1.42,
        "mbps": 5900.82,
        "integrity": true
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.2
      },
      "concurrent": [
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 2.97,
          "mbps": 2821.5,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 3.28,
          "mbps": 2558.75,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 3.04,
          "mbps": 2763.87,
          "integrity": true
        }
      ]
    }
  },
  {
    "id": "eb2e7bbdb8d2",
    "time": "2026-11-19T10:29:00.989562+00:00",
    "scenario": "tcp_off",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "TCP_UNAVAILABLE"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.1"
      },
      "direct_tcp": {
        "ok": false,
        "host": "127.0.0.1",
        "ms": 808.33,
        "error": "TimeoutError",
        "detail": "timed out"
      },
      "domain_tcp": {
        "ok": false,
        "host": "127.0.0.1",
        "ms": 809.74,
        "error": "TimeoutError",
        "detail": "timed out"
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.226
      },
      "concurrent": [
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 808.58,
          "error": "TimeoutError",
          "detail": "timed out"
        },
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 808.56,
          "error": "TimeoutError",
          "detail": "timed out"
        },
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 808.39,
          "error": "TimeoutError",
          "detail": "timed out"
        }
      ]
    }
  },
  {
    "id": "fc3dec5938e6",
    "time": "2026-11-19T10:29:02.184773+00:00",
    "scenario": "delay",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "RESPONSE_DELAY"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.1"
      },
      "direct_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 390.41,
        "mbps": 21.49,
        "integrity": true
      },
      "domain_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 366.59,
        "mbps": 22.88,
        "integrity": true
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.241
      },
      "concurrent": [
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 363.4,
          "mbps": 23.08,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 369.73,
          "mbps": 22.69,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 353.75,
          "mbps": 23.71,
          "integrity": true
        }
      ]
    }
  },
  {
    "id": "62d088e381aa",
    "time": "2026-11-19T10:29:02.791217+00:00",
    "scenario": "udp_loss",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "UDP_LOSS"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.1"
      },
      "direct_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 3.77,
        "mbps": 2224.39,
        "integrity": true
      },
      "domain_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 24.7,
        "mbps": 339.56,
        "integrity": true
      },
      "udp": {
        "sent": 8,
        "received": 4,
        "loss_percent": 50.0,
        "rtt_ms": 0.543
      },
      "concurrent": [
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 2.82,
          "mbps": 2972.15,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 17.95,
          "mbps": 467.44,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 15.42,
          "mbps": 543.96,
          "integrity": true
        }
      ]
    }
  },
  {
    "id": "4531e5ca1253",
    "time": "2026-11-19T10:29:03.695015+00:00",
    "scenario": "dns_wrong",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "DNS_MISMATCH"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.2"
      },
      "direct_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 3.34,
        "mbps": 2510.06,
        "integrity": true
      },
      "domain_tcp": {
        "ok": false,
        "host": "127.0.0.2",
        "ms": 804.98,
        "error": "TimeoutError",
        "detail": "timed out"
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.351
      },
      "concurrent": [
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 13.7,
          "mbps": 612.35,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 3.14,
          "mbps": 2674.34,
          "integrity": true
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 13.31,
          "mbps": 630.18,
          "integrity": true
        }
      ]
    }
  },
  {
    "id": "6f093027cea7",
    "time": "2026-11-19T10:29:03.804968+00:00",
    "scenario": "corrupt",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "FILE_CORRUPTED"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.1"
      },
      "direct_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 3.28,
        "mbps": 2560.63,
        "integrity": false
      },
      "domain_tcp": {
        "ok": true,
        "host": "127.0.0.1",
        "bytes": 1048576,
        "ms": 3.13,
        "mbps": 2680.84,
        "integrity": false
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.213
      },
      "concurrent": [
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 4.49,
          "mbps": 1867.25,
          "integrity": false
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 4.34,
          "mbps": 1932.55,
          "integrity": false
        },
        {
          "ok": true,
          "host": "127.0.0.1",
          "bytes": 1048576,
          "ms": 21.15,
          "mbps": 396.7,
          "integrity": false
        }
      ]
    }
  },
  {
    "id": "b6a2ea81da93",
    "time": "2026-11-19T10:29:06.296811+00:00",
    "scenario": "combined",
    "ports": {
      "tcp": 19090,
      "udp": 19091,
      "dns": 15353
    },
    "findings": [
      "DNS_MISMATCH",
      "TCP_UNAVAILABLE"
    ],
    "evidence": {
      "dns": {
        "ok": true,
        "address": "127.0.0.2"
      },
      "direct_tcp": {
        "ok": false,
        "host": "127.0.0.1",
        "ms": 809.62,
        "error": "TimeoutError",
        "detail": "timed out"
      },
      "domain_tcp": {
        "ok": false,
        "host": "127.0.0.2",
        "ms": 811.27,
        "error": "TimeoutError",
        "detail": "timed out"
      },
      "udp": {
        "sent": 8,
        "received": 8,
        "loss_percent": 0.0,
        "rtt_ms": 0.496
      },
      "concurrent": [
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 804.56,
          "error": "TimeoutError",
          "detail": "timed out"
        },
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 804.34,
          "error": "TimeoutError",
          "detail": "timed out"
        },
        {
          "ok": false,
          "host": "127.0.0.1",
          "ms": 804.05,
          "error": "TimeoutError",
          "detail": "timed out"
        }
      ]
    }
  }
];
