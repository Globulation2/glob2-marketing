#!/usr/bin/env python3
"""Allowlist HTTPS proxy for the sandboxed Claude agents (README "Security and sandboxing").

The agent user's packets may only go to loopback (nftables rule from install-agent-sandbox.sh),
so the only way out is this proxy, which runs as the operator on 127.0.0.1. It accepts
`CONNECT host:443` for allowlisted hosts and refuses everything else: other hosts, other ports,
plain-HTTP requests and IP-literal targets. Every decision is logged, one JSON line each.

  egress_proxy.py [--port 3129] [--allow HOST ...] [--log FILE]

The default allowlist is the Anthropic API host that Claude Code needs when it signs in with
a long-lived OAuth token (CLAUDE_CODE_OAUTH_TOKEN) and runs with nonessential traffic,
telemetry, error reporting, feature flags and updates turned off. Add hosts with
EGRESS_ALLOW (space-separated) or --allow. Standard library only.
"""
import argparse
import datetime
import ipaddress
import json
import os
import select
import socket
import sys
import threading

DEFAULT_ALLOW = ("api.anthropic.com",)
MAX_HEADER = 16384
IDLE_TIMEOUT = 600  # seconds without traffic before a tunnel is closed


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Proxy:
    def __init__(self, allow, log_path):
        self.allow = {h.lower().rstrip(".") for h in allow}
        self.log_path = log_path
        self.lock = threading.Lock()

    def log(self, **event):
        line = json.dumps({"at": now(), **event})
        with self.lock:
            if self.log_path:
                with open(self.log_path, "a") as fh:
                    fh.write(line + "\n")
            else:
                print(line, flush=True)

    def allowed(self, host: str, port: int) -> bool:
        if port != 443:
            return False
        try:
            ipaddress.ip_address(host.strip("[]"))
            return False            # never tunnel to raw IPs: the allowlist is by name
        except ValueError:
            pass
        return host.lower().rstrip(".") in self.allow

    def handle(self, client: socket.socket, peer):
        try:
            client.settimeout(30)
            head = b""
            while b"\r\n\r\n" not in head:
                chunk = client.recv(4096)
                if not chunk:
                    return
                head += chunk
                if len(head) > MAX_HEADER:
                    return self.refuse(client, peer, "", 0, "header too large", 431)
            request_line = head.split(b"\r\n", 1)[0].decode("latin-1")
            parts = request_line.split()
            if len(parts) != 3 or parts[0].upper() != "CONNECT":
                return self.refuse(client, peer, request_line[:80], 0, "only CONNECT is allowed", 405)
            host, _, port = parts[1].rpartition(":")
            try:
                port = int(port)
            except ValueError:
                return self.refuse(client, peer, parts[1][:80], 0, "bad target", 400)
            if not self.allowed(host, port):
                return self.refuse(client, peer, host, port, "not on the allowlist", 403)
            try:
                upstream = socket.create_connection((host, port), timeout=30)
            except OSError as e:
                self.log(decision="error", host=host, port=port, error=type(e).__name__)
                client.sendall(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n")
                return
            self.log(decision="allow", host=host, port=port)
            client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            rest = head.split(b"\r\n\r\n", 1)[1]
            if rest:
                upstream.sendall(rest)
            self.pipe(client, upstream)
        except OSError:
            pass
        finally:
            client.close()

    def refuse(self, client, peer, host, port, reason, code):
        self.log(decision="refuse", host=host, port=port, reason=reason)
        msg = {403: "Forbidden", 405: "Method Not Allowed", 400: "Bad Request", 431: "Header Too Large"}[code]
        try:
            client.sendall(f"HTTP/1.1 {code} {msg}\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode())
        except OSError:
            pass

    @staticmethod
    def pipe(a: socket.socket, b: socket.socket):
        socks = [a, b]
        try:
            while True:
                ready, _, _ = select.select(socks, [], [], IDLE_TIMEOUT)
                if not ready:
                    return
                for s in ready:
                    data = s.recv(65536)
                    if not data:
                        return
                    (b if s is a else a).sendall(data)
        finally:
            b.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=int(os.environ.get("EGRESS_PROXY_PORT", "3129")))
    ap.add_argument("--allow", nargs="*", default=None, help="hosts to allow (port 443 only)")
    ap.add_argument("--log", default=os.environ.get("EGRESS_PROXY_LOG", ""), help="append JSON lines here")
    a = ap.parse_args()
    allow = a.allow if a.allow is not None else (os.environ.get("EGRESS_ALLOW", "").split() or list(DEFAULT_ALLOW))
    proxy = Proxy(allow, a.log or None)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", a.port))   # loopback only
    srv.listen(64)
    proxy.log(decision="start", port=a.port, allow=sorted(proxy.allow))
    try:
        while True:
            client, peer = srv.accept()
            threading.Thread(target=proxy.handle, args=(client, peer), daemon=True).start()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())
