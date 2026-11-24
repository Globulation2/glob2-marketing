#!/usr/bin/env python3
"""Minimal Twitch chat (IRC over TLS) client for the stream rig. Standard library only.

    twitch_chat.py listen          print chat messages as JSON lines (and log them)
    twitch_chat.py send TEXT       send one message (needs TWITCH_BOT_USER and a token file)

Without TWITCH_BOT_USER and a mode-600 token file at TWITCH_CHAT_TOKEN_FILE it logs in
anonymously (read-only). The token is never printed or logged.
"""
import argparse
import datetime
import json
import os
import pathlib
import random
import socket
import ssl
import stat
import sys
import threading
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rigconfig  # noqa: E402
import token_refresh  # noqa: E402

HOST, PORT = "irc.chat.twitch.tv", 6697
MAX_LEN = 450
MIN_SEND_GAP = 2.0           # hard floor between our own messages, seconds
LOG_CAP_BYTES = 20 * 1024 * 1024


class TokenError(Exception):
    pass


def read_token(path: str) -> str:
    """Return the OAuth token (without 'oauth:'), refusing files others can read."""
    p = pathlib.Path(path)
    mode = stat.S_IMODE(p.stat().st_mode)
    if mode & 0o077:
        raise TokenError(f"{path} must be mode 600 (is {oct(mode)}); run chmod 600 on it")
    tok = p.read_text().strip()
    if tok.startswith("oauth:"):
        tok = tok[len("oauth:"):]
    if not tok or not tok.replace("_", "").isalnum():
        raise TokenError(f"{path} does not look like a Twitch access token")
    return tok


def parse_tags(raw: str) -> dict:
    tags = {}
    for part in raw.split(";"):
        k, _, v = part.partition("=")
        tags[k] = v.replace("\\s", " ").replace("\\:", ";").replace("\\\\", "\\").replace("\\r", "").replace("\\n", "")
    return tags


def parse_line(line: str) -> dict:
    """Split one IRC line into tags, prefix, command, params, trailing."""
    tags, prefix = {}, ""
    if line.startswith("@"):
        raw, _, line = line[1:].partition(" ")
        tags = parse_tags(raw)
    if line.startswith(":"):
        prefix, _, line = line[1:].partition(" ")
    trailing = None
    if " :" in line:
        line, _, trailing = line.partition(" :")
    parts = line.split()
    return {"tags": tags, "prefix": prefix, "command": parts[0] if parts else "",
            "params": parts[1:], "trailing": trailing}


def clean_text(text: str) -> str:
    text = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    return text[:MAX_LEN]


class TwitchChat:
    """Connects, joins one channel, yields messages; reconnects with backoff."""

    def __init__(self, channel: str, user: str = "", token_file: str = "", log_dir: str = "",
                 cli_env: str = None):
        self.channel = channel.lower().lstrip("#")
        self.user, self._token, self.token_file, self.refresher = "", "", token_file, None
        cli_env = cli_env or token_refresh.default_cli_env()
        if user and token_file and (os.path.exists(token_file) or os.path.exists(cli_env)):
            self.user = user.lower()
            if os.path.exists(cli_env):
                self.refresher = token_refresh.TokenRefresher(token_file, cli_env)
            if os.path.exists(token_file):
                self._token = read_token(token_file)
        self.can_send = bool(self.user)
        self._auth_retry = False
        self.nick = self.user or f"justinfan{random.randint(10000, 99999)}"
        self.log_dir = pathlib.Path(log_dir) / "chat" if log_dir else None
        self.connected = False
        self.joined = threading.Event()
        self._sock = None
        self._buf = b""
        self._send_lock = threading.Lock()
        self._last_send = 0.0

    # -- connection -------------------------------------------------------------
    def refresh_token(self, force: bool = False):
        """Keep the token file fresh through the Twitch CLI (if configured) and reload it."""
        if not self.user:
            return
        if self.refresher:
            try:
                if force:
                    self.refresher.refresh()
                else:
                    self.refresher.ensure()
            except (token_refresh.RefreshError, OSError) as e:
                print(f"twitch_chat: token refresh failed: {e}", file=sys.stderr)
        self._token = read_token(self.token_file)

    def start_refresh_watch(self, interval: float = 600):
        """Re-check the token every `interval` seconds so reconnects always have a fresh one."""
        def loop():
            while True:
                time.sleep(interval)
                try:
                    self.refresh_token()
                except (OSError, TokenError) as e:
                    print(f"twitch_chat: token check failed: {e}", file=sys.stderr)
        if self.refresher:
            threading.Thread(target=loop, daemon=True).start()

    def connect(self):
        self.refresh_token()
        ctx = ssl.create_default_context()
        raw = socket.create_connection((HOST, PORT), timeout=30)
        self._sock = ctx.wrap_socket(raw, server_hostname=HOST)
        self._sock.settimeout(360)          # Twitch PINGs about every 5 minutes
        self._buf = b""
        self.joined.clear()
        self._raw("CAP REQ :twitch.tv/tags twitch.tv/commands")
        self._raw(f"PASS oauth:{self._token}" if self._token else "PASS SCHMOOPIIE", secret=True)
        self._raw(f"NICK {self.nick}")
        self._raw(f"JOIN #{self.channel}")
        self.connected = True

    def close(self):
        self.connected = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        self._sock = None

    def _raw(self, line: str, secret: bool = False):
        self._sock.sendall((line + "\r\n").encode("utf-8"))

    def _lines(self):
        while True:
            while b"\r\n" not in self._buf:
                chunk = self._sock.recv(65536)
                if not chunk:
                    raise ConnectionError("server closed the connection")
                self._buf += chunk
            line, self._buf = self._buf.split(b"\r\n", 1)
            yield line.decode("utf-8", "replace")

    # -- messages ---------------------------------------------------------------
    def messages(self, reconnect: bool = True):
        """Yield chat messages as dicts: at, user, display, text, id, mod, badges."""
        backoff = 1
        while True:
            try:
                if not self.connected:
                    self.connect()
                for line in self._lines():
                    m = parse_line(line)
                    cmd = m["command"]
                    if cmd == "PING":
                        self._raw(f"PONG :{m['trailing'] or 'tmi.twitch.tv'}")
                    elif cmd == "RECONNECT":
                        raise ConnectionError("server asked to reconnect")
                    elif cmd == "NOTICE" and any(k in (m["trailing"] or "").lower()
                                                 for k in ("authentication failed", "improperly formatted auth")):
                        if self.refresher and not self._auth_retry:
                            self._auth_retry = True
                            self.refresh_token(force=True)
                            raise ConnectionError("chat token rejected; refreshed it, reconnecting")
                        raise TokenError("Twitch rejected the chat token (login authentication failed)")
                    elif cmd in ("JOIN", "ROOMSTATE") and m["params"] and m["params"][0].lower() == f"#{self.channel}":
                        if cmd == "ROOMSTATE" or m["prefix"].split("!")[0].lower() == self.nick:
                            self.joined.set()
                            self._auth_retry = False
                            backoff = 1
                    elif cmd == "PRIVMSG" and m["trailing"] is not None:
                        t = m["tags"]
                        msg = {
                            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                            "user": m["prefix"].split("!")[0].lower(),
                            "display": t.get("display-name") or m["prefix"].split("!")[0],
                            "text": m["trailing"],
                            "id": t.get("id", ""),
                            "mod": t.get("mod") == "1" or "broadcaster/" in t.get("badges", ""),
                            "badges": t.get("badges", ""),
                        }
                        self._log(msg)
                        yield msg
            except TokenError:
                self.close()
                raise
            except (OSError, ConnectionError, ssl.SSLError) as e:
                self.close()
                if not reconnect:
                    raise
                print(f"twitch_chat: {type(e).__name__}: {e}; reconnecting in {backoff}s", file=sys.stderr)
                time.sleep(backoff)
                backoff = min(backoff * 2, 120)

    def send(self, text: str) -> str:
        """Send one message to the channel; returns the text actually sent."""
        if not self.can_send:
            raise PermissionError("read-only: set TWITCH_BOT_USER and a mode-600 token file to send")
        text = clean_text(text)
        if not text:
            return ""
        if text.startswith(("/", ".")):     # never issue chat commands
            text = " " + text
        with self._send_lock:
            wait = MIN_SEND_GAP - (time.monotonic() - self._last_send)
            if wait > 0:
                time.sleep(wait)
            self._raw(f"PRIVMSG #{self.channel} :{text}")
            self._last_send = time.monotonic()
        self._log({"at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                   "user": self.user, "display": self.user, "text": text, "own": True})
        return text

    def _log(self, msg: dict):
        if not self.log_dir:
            return
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            f = self.log_dir / f"{datetime.date.today().isoformat()}.jsonl"
            if f.exists() and f.stat().st_size > LOG_CAP_BYTES:
                return
            with f.open("a") as fh:
                fh.write(json.dumps(msg, ensure_ascii=False) + "\n")
        except OSError:
            pass


def from_config(cfg: dict = None, log: bool = True) -> TwitchChat:
    cfg = cfg or rigconfig.load()
    return TwitchChat(cfg["TWITCH_CHANNEL"], cfg.get("TWITCH_BOT_USER", ""),
                      cfg.get("TWITCH_CHAT_TOKEN_FILE", ""), cfg["LOG_DIR"] if log else "",
                      os.environ.get("TWITCH_CLI_ENV") or cfg.get("TWITCH_CLI_ENV") or None)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listen", help="print chat messages as JSON lines")
    s = sub.add_parser("send", help="send one message")
    s.add_argument("text", nargs="+")
    ap.add_argument("--channel", help="override TWITCH_CHANNEL")
    ap.add_argument("--no-log", action="store_true", help="do not write the chat log")
    a = ap.parse_args()
    cfg = rigconfig.load()
    if a.channel:
        cfg["TWITCH_CHANNEL"] = a.channel
    try:
        chat = from_config(cfg, log=not a.no_log)
        if a.cmd == "listen":
            print(f"listening to #{chat.channel} as {'read-only guest' if not chat.can_send else chat.user}", file=sys.stderr)
            for msg in chat.messages():
                print(json.dumps(msg, ensure_ascii=False), flush=True)
        else:
            if not chat.can_send:
                sys.exit("read-only: set TWITCH_BOT_USER and install the token at TWITCH_CHAT_TOKEN_FILE (mode 600)")
            chat.connect()
            failure = []

            def drain():
                try:
                    for _ in chat.messages(reconnect=False):
                        pass
                except Exception as e:  # reported below
                    failure.append(e)
                    chat.joined.set()
            threading.Thread(target=drain, daemon=True).start()
            if not chat.joined.wait(15) or failure:
                sys.exit(f"twitch_chat: could not join #{chat.channel}: {failure[0] if failure else 'timed out'}")
            sent = chat.send(" ".join(a.text))
            time.sleep(1)
            print(f"sent: {sent}")
    except TokenError as e:
        sys.exit(f"twitch_chat: {e}")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
