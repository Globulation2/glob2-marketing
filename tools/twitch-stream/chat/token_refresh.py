#!/usr/bin/env python3
"""Keep the Twitch chat token fresh using the Twitch CLI's saved refresh token.

    token_refresh.py status     validate the installed token (login, scopes, minutes left)
    token_refresh.py ensure     refresh only if invalid or under 30 minutes left
    token_refresh.py refresh    refresh now
    token_refresh.py login-url  print a browser login link (for logging in from another machine)
    token_refresh.py redeem URL install the login from the localhost:3000/?code=... address the browser
                                ends on (it fails to load off the stream machine; copy it anyway)

The Twitch CLI (`twitch`, configured with `twitch configure` and logged in with
`twitch token -u -s 'chat:read chat:edit channel:manage:broadcast clips:edit'`) keeps CLIENTID, CLIENTSECRET,
ACCESSTOKEN, REFRESHTOKEN and TOKENEXPIRATION in TWITCH_CLI_ENV. Refreshing posts
those credentials to Twitch's token endpoint over HTTPS (the same request
`twitch token -R` makes), so no secret ever appears in a process's arguments. It then
writes the new tokens back to that file and installs the access token atomically
(mode 600) at TWITCH_CHAT_TOKEN_FILE. Tokens never reach stdout, stderr or logs.
"""
import datetime
import json
import os
import pathlib
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import rigconfig  # noqa: E402

VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
REFRESH_BELOW = 30 * 60          # seconds of validity left that triggers a refresh


class RefreshError(Exception):
    pass


def default_cli_env() -> str:
    return os.environ.get("TWITCH_CLI_ENV") or str(pathlib.Path.home() / ".config/twitch-cli/.twitch-cli.env")


def read_env(path: str) -> dict:
    try:
        lines = pathlib.Path(path).read_text().splitlines()
    except OSError as e:
        raise RefreshError(f"cannot read the Twitch CLI settings at {path} ({e.strerror}); "
                           "run `twitch configure` and `twitch token -u -s 'chat:read chat:edit channel:manage:broadcast clips:edit'`") from None
    return dict(line.split("=", 1) for line in lines if "=" in line)


def validate(token: str) -> dict | None:
    """Return Twitch's validation (login, scopes, expires_in), or None if the token is invalid."""
    req = urllib.request.Request(VALIDATE_URL, headers={"Authorization": f"OAuth {token}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return None
        raise


def install_token(token: str, path: str):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=p.name + ".")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(token + "\n")
        os.replace(tmp, p)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


def update_env(path: str, values: dict):
    """Rewrite KEY=VALUE lines of the Twitch CLI file atomically, keeping its other lines and mode."""
    p = pathlib.Path(path)
    lines, seen = [], set()
    for line in p.read_text().splitlines():
        key = line.split("=", 1)[0]
        if key in values:
            line, _ = f"{key}={values[key]}", seen.add(key)
        lines.append(line)
    lines += [f"{k}={v}" for k, v in values.items() if k not in seen]
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=p.name + ".")
    try:
        os.fchmod(fd, p.stat().st_mode & 0o777)
        with os.fdopen(fd, "w") as f:
            f.write("\n".join(lines) + "\n")
        os.replace(tmp, p)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


def _redact(text: str, secrets) -> str:
    for s in secrets:
        if s:
            text = text.replace(s, "<redacted>")
    return text


class TokenRefresher:
    def __init__(self, token_file: str, cli_env: str = None, cli: str = None, expect_login: str = ""):
        self.token_file = token_file
        self.expect_login = (expect_login or "").lower()   # refuse a token for any other account
        self.cli_env = cli_env or default_cli_env()
        del cli  # kept for compatibility: refreshing no longer runs the Twitch CLI

    def current(self) -> str:
        try:
            return pathlib.Path(self.token_file).read_text().strip().removeprefix("oauth:")
        except OSError:
            return ""

    def refresh(self) -> dict:
        """Refresh with the Twitch CLI's saved credentials and install the new access token."""
        env = read_env(self.cli_env)
        need = [k for k in ("CLIENTID", "CLIENTSECRET", "REFRESHTOKEN") if not env.get(k)]
        if need:
            raise RefreshError(f"{self.cli_env} lacks {', '.join(need)}; run `twitch configure` and "
                               "`twitch token -u -s 'chat:read chat:edit channel:manage:broadcast clips:edit'`")
        body = urllib.parse.urlencode({"client_id": env["CLIENTID"], "client_secret": env["CLIENTSECRET"],
                                       "grant_type": "refresh_token", "refresh_token": env["REFRESHTOKEN"]}).encode()
        try:
            with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, body), timeout=30) as resp:
                got = json.load(resp)
        except urllib.error.HTTPError as e:
            raise RefreshError(f"Twitch refused the refresh (HTTP {e.code}); log in again with "
                               "`twitch token -u -s 'chat:read chat:edit channel:manage:broadcast clips:edit'`") from None
        new = got.get("access_token", "")
        info = validate(new) if new else None
        if info is None:
            raise RefreshError("Twitch returned no usable access token")
        self.check_login(info)
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=int(got.get("expires_in", 0)))
        update_env(self.cli_env, {"ACCESSTOKEN": new, "REFRESHTOKEN": got.get("refresh_token") or env["REFRESHTOKEN"],
                                  "TOKENEXPIRATION": expires.strftime("%Y-%m-%dT%H:%M:%SZ")})
        install_token(new, self.token_file)
        return info

    def check_login(self, info: dict):
        """A login authorized in a browser signed in to another account (it happened on 2026-11-26)
        must never be installed or used: it would chat, title and clip as that account."""
        if self.expect_login and info.get("login", "").lower() != self.expect_login:
            raise RefreshError(f"the token belongs to {info.get('login')}, not {self.expect_login}; log in "
                               f"again as {self.expect_login} (a private window avoids a signed-in account)")

    def ensure(self, below: int = REFRESH_BELOW) -> tuple:
        """Refresh if the installed token is missing, invalid or close to expiry. Returns (info, refreshed)."""
        tok = self.current()
        info = validate(tok) if tok else None
        if info and info.get("expires_in", 0) >= below:
            self.check_login(info)
            return info, False
        return self.refresh(), True


def from_config(cfg: dict = None) -> TokenRefresher:
    cfg = cfg or rigconfig.load()
    return TokenRefresher(cfg["TWITCH_CHAT_TOKEN_FILE"], os.environ.get("TWITCH_CLI_ENV") or cfg.get("TWITCH_CLI_ENV"),
                          expect_login=cfg.get("TWITCH_BOT_USER") or cfg.get("TWITCH_CHANNEL", ""))


SCOPES = "chat:read chat:edit channel:manage:broadcast clips:edit"
REDIRECT = "http://localhost:3000"


def login_url(r: "TokenRefresher") -> str:
    """force_verify makes Twitch show which account is signing in, so a browser signed in to the
    owner's personal account is noticed before it authorizes the wrong one."""
    import secrets
    env = read_env(r.cli_env)
    return "https://id.twitch.tv/oauth2/authorize?" + urllib.parse.urlencode({
        "client_id": env["CLIENTID"], "redirect_uri": REDIRECT, "response_type": "code",
        "scope": SCOPES, "force_verify": "true", "state": secrets.token_urlsafe(12)})


def redeem(r: "TokenRefresher", address: str) -> dict:
    """Trade the one-time code for tokens, check the account, then install them."""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(address).query)
    code = (q.get("code") or [address.strip()])[0]
    env = read_env(r.cli_env)
    body = urllib.parse.urlencode({"client_id": env["CLIENTID"], "client_secret": env["CLIENTSECRET"], "code": code,
                                   "grant_type": "authorization_code", "redirect_uri": REDIRECT}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, body), timeout=30) as resp:
            got = json.load(resp)
    except urllib.error.HTTPError as e:
        raise RefreshError(f"Twitch refused the code (HTTP {e.code}); codes work once, for a few minutes") from None
    info = validate(got.get("access_token", ""))
    if info is None:
        raise RefreshError("Twitch returned no usable access token")
    r.check_login(info)   # before anything is written
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=int(got.get("expires_in", 0)))
    update_env(r.cli_env, {"ACCESSTOKEN": got["access_token"], "REFRESHTOKEN": got["refresh_token"],
                           "TOKENEXPIRATION": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "TOKENSCOPES": "[" + " ".join(sorted(info.get("scopes", []))) + "]"})
    install_token(got["access_token"], r.token_file)
    return info


def describe(info: dict) -> str:
    return f"login {info.get('login')}, scopes {' '.join(info.get('scopes', []))}, {info.get('expires_in', 0) // 60} min left"


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    r = from_config()
    try:
        if cmd == "status":
            tok = r.current()
            info = validate(tok) if tok else None
            print(describe(info) if info else "no valid token installed")
            sys.exit(0 if info else 1)
        elif cmd == "ensure":
            info, refreshed = r.ensure()
            print(("refreshed: " if refreshed else "still valid: ") + describe(info))
        elif cmd == "refresh":
            print("refreshed: " + describe(r.refresh()))
        elif cmd == "login-url":
            print(login_url(r))
        elif cmd == "redeem" and len(sys.argv) > 2:
            print("installed: " + describe(redeem(r, sys.argv[2])))
        else:
            sys.exit(__doc__)
    except (RefreshError, urllib.error.URLError) as e:
        sys.exit(f"token_refresh: {e}")


if __name__ == "__main__":
    main()
