#!/usr/bin/env python3
"""Run Claude Plays Glob continuously: game, stream, one player session per match, optional chat agent.

  supervisor.py run [--stream none|file:PATH|live] [--i-mean-it] [--chat]
                    [--max-games N] [--game-timeout MIN] [--down]

--stream none (default) plays without capturing; file:PATH records locally; live
broadcasts to Twitch and needs --i-mean-it (and the user's go-ahead). Stop with
Ctrl-C, SIGTERM or down.sh. Each match gets a fresh, sandboxed `claude -p` session
(see prompts/player.md): only the game's MCP tools, the stream-ctl match tools
and file tools confined to the notes directory. The chat agent, when enabled, is
a separate process (chat/chat_agent.py) that never touches the game.
"""
import argparse
import gzip
import json
import logging
import logging.handlers
import os
import pathlib
import shutil
import signal
import subprocess
import sys
import threading
import time
import re
import urllib.request

# A control token in the player transcript (JSON, possibly escaped inside a tool result).
TOKEN_RE = re.compile(rb'\\?"token\\?":\s*\\?"([A-Za-z0-9+/]{20,}={0,2})')

import rigconfig
import rigstate

SESSION_RETRIES = 3          # sessions per match before the supervisor records it aborted
KEEP_PLAYER_LOGS = 100
LOG_CAP_BYTES = 20 * 1024 * 1024
MIN_FREE_BYTES = 2 * 1024 ** 3
log = logging.getLogger("supervisor")


def check_sandbox(cfg: dict) -> None:
    """With AGENT_USER set, the sandbox must be installed before anything else starts."""
    if not cfg["AGENT_USER"]:
        return
    agent_run = pathlib.Path(cfg["AGENT_INSTALL_DIR"]) / "agent-run"
    if not agent_run.exists():
        sys.exit(f"agent sandbox not installed ({agent_run} missing): run sandbox/install-agent-sandbox.sh, "
                 "or set AGENT_USER=\"\" in stream.env to run the agents unsandboxed (less isolated)")
    for key in ("NOTES_DIR", "STATE_DIR"):
        if not os.access(cfg[key], os.W_OK):
            sys.exit(f"{key} {cfg[key]} is not writable: rerun sandbox/install-agent-sandbox.sh")


class Supervisor:
    def __init__(self, args):
        self.args = args
        self.cfg = rigconfig.load()
        check_sandbox(self.cfg)
        self.rig = pathlib.Path(self.cfg["RIG_DIR"])
        self.log_dir = pathlib.Path(self.cfg["LOG_DIR"])
        self.notes = pathlib.Path(self.cfg["NOTES_DIR"])
        self.state = rigstate.state_dir(self.cfg)
        self.player_logs = self.log_dir / "player"
        for d in (self.log_dir, self.notes, self.player_logs):
            d.mkdir(parents=True, exist_ok=True)
        self.env = {**os.environ, **self.cfg}
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.stream_proc = self.stream_since = None
        self.chat_proc = None
        self.player_proc = self.player_since = None
        self.started = rigstate.now()
        self.mode = args.stream.split(":", 1)[0]
        self.low_disk = False
        self.player_token = None

    # --- helpers ------------------------------------------------------------------
    def mcp(self, tool, arguments=None, timeout=5):
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                           "params": {"name": tool, "arguments": arguments or {}}}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{self.cfg['MCP_PORT']}/mcp", body, {
            "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25", "Mcp-Method": "tools/call", "Mcp-Name": tool})
        out = json.load(urllib.request.urlopen(req, timeout=timeout))
        return json.loads(out["result"]["content"][0]["text"])

    def run_script(self, name, *args):
        return subprocess.run([str(self.rig / name), *args], env=self.env, capture_output=True, text=True)

    def sleep(self, seconds):
        return self.stop.wait(seconds)

    @staticmethod
    def terminate(proc, sig=signal.SIGTERM, grace=20, group=False):
        if not proc or proc.poll() is not None:
            return
        # With the sandbox, the group holds sudo (ours) and the agent (another user, which we may not
        # signal): sudo relays the signal, and agent-run's parent-death signal covers a killed sudo.
        try:
            (os.killpg if group else os.kill)(proc.pid, sig)
            proc.wait(grace)
        except (ProcessLookupError, PermissionError, subprocess.TimeoutExpired):
            try:
                (os.killpg if group else os.kill)(proc.pid, signal.SIGKILL)
                proc.wait(5)
            except (ProcessLookupError, PermissionError, subprocess.TimeoutExpired):
                pass

    # --- game ---------------------------------------------------------------------
    def ensure_game(self):
        out = self.run_script("game-up.sh")
        if out.returncode:
            log.error("game-up.sh failed: %s", (out.stdout + out.stderr).strip()[-500:])
            return False
        want = tuple(int(v) for v in self.cfg["STREAM_SIZE"].split("x"))
        try:
            st = self.mcp("ui_status")
        except Exception as exc:  # noqa: BLE001 - any failure means the game is not usable
            log.error("game MCP not answering: %s", exc)
            return False
        if (st.get("width"), st.get("height")) != want:
            log.warning("game window is %sx%s, want %dx%d; restarting the game", st.get("width"), st.get("height"), *want)
            pid_file = self.log_dir / "game.pid"
            if pid_file.exists():
                try:
                    os.kill(int(pid_file.read_text()), signal.SIGTERM)
                except (ValueError, ProcessLookupError):
                    pass
            time.sleep(3)
            return self.run_script("game-up.sh").returncode == 0
        return True

    # --- stream and chat children ------------------------------------------------------
    def stream_loop(self):
        if self.mode == "none":
            return
        failures = 0
        while not self.stop.is_set():
            if self.low_disk and self.mode == "file":
                return
            if self.mode == "file":
                cmd = [str(self.rig / "stream.sh"), "file", self.args.stream.split(":", 1)[1], str(7 * 24 * 3600)]
            else:
                cmd = [str(self.rig / "stream.sh"), "live", "--i-mean-it"]
            with open(self.log_dir / "stream-supervised.log", "ab") as err:
                proc = subprocess.Popen(cmd, env=self.env, stdin=subprocess.DEVNULL, stdout=err, stderr=err)
            with self.lock:
                self.stream_proc, self.stream_since = proc, rigstate.now()
            log.info("stream %s started (pid %d)", self.mode, proc.pid)
            began = time.time()
            while proc.poll() is None and not self.stop.is_set():
                self.sleep(2)
            with self.lock:
                self.stream_proc = self.stream_since = None
            if self.stop.is_set():
                self.terminate(proc, signal.SIGINT, grace=15)  # SIGINT lets ffmpeg finalize the file
                return
            log.warning("stream exited with %s", proc.returncode)
            if self.mode == "file":
                return  # a recording is not restarted over itself
            failures = failures + 1 if time.time() - began < 120 else 1
            self.sleep(min(10 * 2 ** (failures - 1), 300))

    def chat_loop(self):
        script = self.rig / "chat" / "chat_agent.py"
        failures = 0
        while not self.stop.is_set():
            if not script.exists():
                log.error("chat agent %s not found; chat disabled", script)
                return
            cmd = [sys.executable, str(script)] + ([] if self.mode == "live" else ["--dry-run"])
            with open(self.log_dir / "chat.log", "ab") as out:
                proc = subprocess.Popen(cmd, env=self.env, stdin=subprocess.DEVNULL, stdout=out, stderr=out,
                                        start_new_session=True)
            with self.lock:
                self.chat_proc = proc
            log.info("chat agent started (pid %d)%s", proc.pid, "" if self.mode == "live" else " in dry-run")
            began = time.time()
            while proc.poll() is None and not self.stop.is_set():
                self.sleep(2)
            if self.stop.is_set():
                self.terminate(proc, group=True)
                return
            log.warning("chat agent exited with %s", proc.returncode)
            failures = failures + 1 if time.time() - began < 120 else 1
            if self.chat_fatal(began):
                failures = max(failures, 6)  # bad token or similar: retry in minutes, not seconds
            self.sleep(min(15 * 2 ** (failures - 1), 600))

    def chat_fatal(self, since) -> bool:
        """The chat agent prints a line starting 'chat_agent:' before a fatal exit (for example a bad token)."""
        path = self.log_dir / "chat.log"
        try:
            if path.stat().st_mtime < since:
                return False
            with open(path, "rb") as fh:
                fh.seek(max(0, path.stat().st_size - 4096))
                tail = fh.read().decode("utf-8", "replace")
        except OSError:
            return False
        return any(line.startswith("chat_agent:") for line in tail.splitlines()[-5:])

    # --- status ---------------------------------------------------------------------------
    def status_loop(self):
        tick = 0
        while not self.stop.is_set():
            try:
                self.write_status(inspect=tick % 3 == 0)
                self.housekeeping()
            except Exception:  # noqa: BLE001 - status must never stop the supervisor
                log.exception("status update failed")
            tick += 1
            self.sleep(10)

    def write_status(self, inspect=True, mode=None):
        game = {"mcp": False, "screen": None}
        try:
            self.mcp("ui_status", timeout=3)
            game["mcp"] = True
            if inspect:
                game["screen"] = self.mcp("ui_inspect", {"compact": True}, timeout=5).get("inspection", {}).get("screen")
            else:
                game["screen"] = (rigstate.read_json(self.state / "status.json", {}) or {}).get("game", {}).get("screen")
        except Exception:  # noqa: BLE001
            pass
        cur = rigstate.current(self.cfg)
        games = rigstate.games(self.cfg)
        with self.lock:
            stream_running = bool(self.stream_proc and self.stream_proc.poll() is None)
            stream_since, player_since = self.stream_since, self.player_since
            player_running = bool(self.player_proc and self.player_proc.poll() is None)
        opp = cur.get("opponent")
        status = {
            "updated": rigstate.now(),
            "mode": mode or self.mode,
            "stream": {"running": stream_running, "since": stream_since if stream_running else None},
            "game": game,
            "match": {"number": cur.get("number"), "opponent": opp,
                      "record": rigstate.record(games, opp) if opp else None,
                      "generator": cur.get("generator"), "goal": cur.get("goal"),
                      "last_move": cur.get("last_move"),
                      "phase": "offline" if mode == "offline" else cur.get("phase", "setup")},
            "player_agent": {"running": player_running, "since": player_since if player_running else None},
            "supervisor": {"pid": os.getpid(), "since": self.started, "low_disk": self.low_disk},
        }
        rigstate.write_json(self.state / "status.json", status)

    def housekeeping(self):
        for path in [self.log_dir / n for n in ("stream.log", "stream-supervised.log", "chat.log", "file.log", "test.log")] + \
                [self.player_logs / "stderr.log"]:
            if path.exists() and path.stat().st_size > LOG_CAP_BYTES:
                with open(path, "rb") as src, gzip.open(str(path) + ".1.gz", "wb") as dst:
                    shutil.copyfileobj(src, dst)
                os.truncate(path, 0)  # writers append, so they continue at the start
        old = sorted(self.player_logs.glob("match-*.jsonl.gz"))[:-KEEP_PLAYER_LOGS]
        for path in old:
            path.unlink(missing_ok=True)
        self.low_disk = min(shutil.disk_usage(self.log_dir).free, shutil.disk_usage(self.state).free) < MIN_FREE_BYTES
        if self.low_disk and self.mode == "file":
            with self.lock:
                proc = self.stream_proc
            if proc:
                log.error("less than 2 GiB free; stopping the local recording")
                self.terminate(proc, signal.SIGINT, grace=15)

    # --- player sessions ------------------------------------------------------------------
    def mcp_config(self) -> pathlib.Path:
        c = self.cfg
        servers = {
            "glob2-stream": {"type": "http", "url": f"http://127.0.0.1:{c['MCP_PORT']}/mcp"},  # the running game
            "stream-ctl": {"command": sys.executable, "args": [str(self.rig / "stream_ctl.py"), "mcp"],
                           "env": {k: v for k, v in self.cfg.items()}},
        }
        path = self.state / "player-mcp.json"
        rigstate.write_json(path, {"mcpServers": servers})
        return path

    def brief(self, cur, recovery) -> str:
        games = rigstate.games(self.cfg)
        prev = rigstate.previous_generators(games)
        lines = [
            (self.rig / "prompts" / "player.md").read_text(encoding="utf-8").rstrip(),
            "\n---\n",
            (self.rig / "stream-playbook.md").read_text(encoding="utf-8").rstrip(),
            "\n---\n",
            "# This session",
            f"- Match number: {cur['number']}",
            f"- Assigned opponent: **{cur['opponent']}** (your record against it: {rigstate.record(games, cur['opponent'])})",
            f"- Previous map generators, newest first: {', '.join(prev) if prev else 'none yet'}",
            f"- Session started: {rigstate.now()}. Play until the match ends; the supervisor handles any time limits.",
            "- The rig and supervisor handle going live, the stream and Twitch chat; you only play and narrate.",
        ]
        if recovery:
            lines.append(
                "- **Recovery:** an earlier session for this match ended without recording a result, so a match may "
                "already be in progress. Inspect the game first (ui_inspect, game_world). If it is this assigned 1v1 "
                f"against {cur['opponent']} and was set up by the rules, carry on playing it (call match_setup_done "
                "if match_info shows no generator yet). Otherwise leave it through the in-game menu, call "
                "match_result with aborted, and end the session.")
        return "\n".join(lines) + "\n"

    def player_cmd(self, session_id=None):
        if self.cfg["AGENT_USER"]:
            # Sandboxed: agent-run (as AGENT_USER) applies the fixed flags, tools and MCP servers itself.
            cmd = ["sudo", "-n", "-u", self.cfg["AGENT_USER"], f"{self.cfg['AGENT_INSTALL_DIR']}/agent-run",
                   "player", "--model", self.cfg["PLAYER_MODEL"]]
            return cmd + (["--resume", session_id] if session_id else [])
        cmd = ["claude", "-p", "--model", self.cfg["PLAYER_MODEL"], "--restricted",
               "--tools", "Read,Edit,Write", "--strict-mcp-config", "--mcp-config", str(self.mcp_config()),
               "--permission-mode", "dontAsk",
               "--allowedTools", "mcp__glob2-stream__*", "mcp__stream-ctl__*", "Edit(./**)",
               "--output-format", "stream-json", "--verbose"]
        return cmd + (["--resume", session_id] if session_id else [])

    def run_turn(self, cmd, prompt, out_path, deadline):
        """Run one `claude -p` turn; returns (exit code or None if ended by us, session id, cost)."""
        meta = {"session_id": None, "cost": 0.0}
        with open(self.player_logs / "stderr.log", "ab") as err:
            proc = subprocess.Popen(cmd, cwd=self.notes, env=self.env, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=err, start_new_session=True)
        with self.lock:
            self.player_proc = proc
            self.player_since = self.player_since or rigstate.now()

        def pump():
            with gzip.open(out_path, "wb") as dst:
                last_flush = time.time()
                for line in proc.stdout:
                    dst.write(line)
                    if b"token" in line:  # remember the player's control token, to release it later
                        m = TOKEN_RE.search(line)
                        if m:
                            self.player_token = m.group(1).decode()
                    if b'"session_id"' in line or b'"total_cost_usd"' in line:
                        try:
                            msg = json.loads(line)
                            meta["session_id"] = msg.get("session_id") or meta["session_id"]
                            meta["cost"] = msg.get("total_cost_usd") or meta["cost"]
                        except ValueError:
                            pass
                    if time.time() - last_flush > 30:  # keep the transcript readable while the match runs
                        dst.flush()
                        last_flush = time.time()
        pumper = threading.Thread(target=pump, daemon=True)
        pumper.start()
        proc.stdin.write(prompt.encode())
        proc.stdin.close()
        while proc.poll() is None and not self.stop.is_set() and time.time() < deadline:
            self.sleep(2)
        ended_by_us = proc.poll() is None
        if ended_by_us:
            log.warning("ending player session (%s)", "shutdown" if self.stop.is_set() else "game timeout")
            self.terminate(proc, group=True)
        pumper.join(10)
        with self.lock:
            self.player_proc = None
        return (None if ended_by_us else proc.returncode), meta["session_id"], meta["cost"]

    def run_player(self, cur, recovery) -> bool:
        """Play one match: a session, resumed whenever it ends its turn before recording a result."""
        brief = self.brief(cur, recovery)
        rigstate.write_text(self.notes / "session-brief.md", brief, mode=0o644)  # read-only to the agent
        prompt = ("Your full brief for this session follows (also saved as session-brief.md). Play the match.\n\n" + brief)
        deadline = time.time() + self.args.game_timeout * 60
        stamp = time.strftime("%Y%m%d-%H%M%S")
        session_id, part, quick, total_cost = None, 0, 0, 0.0
        log.info("player session for match %d vs %s%s", cur["number"], cur["opponent"], " [recovery]" if recovery else "")
        finished = lambda: any(g.get("number") == cur["number"] for g in rigstate.games(self.cfg))  # noqa: E731
        try:
            while True:
                part += 1
                out_path = self.player_logs / f"match-{stamp}-{cur['number']:05d}-{part:02d}.jsonl.gz"
                began = time.time()
                code, sid, cost = self.run_turn(self.player_cmd(session_id), prompt, out_path, deadline)
                total_cost += cost or 0.0
                session_id = sid or session_id
                log.info("player turn %d exited with %s after %.0f s (cost so far $%.2f)",
                         part, "supervisor stop" if code is None else code, time.time() - began, total_cost)
                if code is None or finished() or code != 0 or not session_id:
                    break
                # The model ended its turn mid-match. Resume the same session instead of starting over.
                quick = quick + 1 if time.time() - began < 60 else 0
                if quick >= 3:
                    log.error("player keeps ending its turn immediately; giving up on this session")
                    break
                prompt = ("The match is not finished: no result is recorded yet, and the stream is still live. "
                          "Keep playing now. Check the game (game_world, ui_status), renew control if needed, "
                          "act, move the camera and narrate. Do not stop or summarise until the game has ended "
                          "and you have called match_result.")
        finally:
            with self.lock:
                self.player_since = None
            self.release_control()
        return finished()

    def release_stale_control(self):
        """At startup, free a lease left by a player session of an earlier supervisor run (one that
        was killed or stopped before it could release), using the token in the newest transcript."""
        token = None
        try:
            newest = max(self.player_logs.glob("*.jsonl.gz"), key=lambda f: f.stat().st_mtime, default=None)
            if newest is None:
                return
            with gzip.open(newest, "rb") as fh:
                for line in fh:
                    m = TOKEN_RE.search(line) if b"token" in line else None
                    if m:
                        token = m.group(1).decode()
        except (OSError, EOFError) as e:  # a truncated transcript still yields what was read
            log.debug("stale control scan: %s", e)
        if token:
            self.player_token = token
            self.release_control()

    def release_control(self):
        """Free the game's control lease the last player session held, so the next session (a
        recovery, or the next match) doesn't wait up to five minutes for it to expire."""
        token, self.player_token = self.player_token, None
        if not token:
            return
        try:
            self.mcp("ui_release_control", {"token": token})
            log.info("released the previous player session's game control")
        except Exception as e:  # already released or expired: nothing to do
            log.debug("release control: %s", e)

    def assign(self):
        cur = rigstate.current(self.cfg)
        games = rigstate.games(self.cfg)
        done = {g.get("number") for g in games}
        if cur.get("number") and cur["number"] not in done and cur.get("opponent") in rigstate.OPPONENTS:
            return cur, True  # unfinished match from an earlier session or supervisor run
        number = max([g.get("number") or 0 for g in games] + [0]) + 1
        cur = {"number": number, "opponent": rigstate.next_opponent(games), "phase": "setup",
               "assigned_at": rigstate.now(), "generator": None, "goal": None, "last_move": None}
        rigstate.save_current(self.cfg, cur)
        return cur, False

    def abandon(self, cur, why):
        log.error("match %d: %s; recording it aborted", cur["number"], why)
        rigstate.append_jsonl(self.state / "games.jsonl", {
            "number": cur["number"], "date": rigstate.now(), "opponent": cur["opponent"],
            "generator": cur.get("generator"), "result": "aborted", "note": f"supervisor: {why}"})
        cur.update(phase="intermission", result="aborted")
        rigstate.save_current(self.cfg, cur)
        self.run_script("caption.sh", "Claude Plays Glob · Between matches\nSetting up the next game")

    def play_loop(self):
        played = attempts = fast_failures = 0
        while not self.stop.is_set() and (not self.args.max_games or played < self.args.max_games):
            if not self.ensure_game():
                fast_failures += 1
                self.sleep(min(30 * 2 ** (fast_failures - 1), 900))
                continue
            cur, recovery = self.assign()
            recovery = recovery or attempts > 0
            rec = rigstate.record(rigstate.games(self.cfg), cur["opponent"])
            if recovery and cur.get("goal"):  # keep the running match's caption
                self.run_script("caption.sh", "--match", cur["opponent"], rec, cur["goal"],
                                *([cur["last_move"]] if cur.get("last_move") else []))
            else:
                self.run_script("caption.sh", "--match", cur["opponent"], rec, "Setting up the next game")
            began = time.time()
            finished = self.run_player(cur, recovery)
            if self.stop.is_set():
                return
            if finished:
                played += 1
                attempts = fast_failures = 0
                self.sleep(20)  # intermission caption stays up briefly
                continue
            attempts += 1
            if attempts >= SESSION_RETRIES:
                self.abandon(cur, f"no result after {attempts} sessions")
                played += 1
                attempts = 0
            fast_failures = fast_failures + 1 if time.time() - began < 120 else 0
            if fast_failures:
                self.sleep(min(30 * 2 ** (fast_failures - 1), 900))

    # --- lifecycle --------------------------------------------------------------------------
    def preflight(self):
        """Fail early and clearly on a missing sandbox or chat token."""
        if not self.cfg["AGENT_USER"]:
            log.warning("AGENT_USER is empty: agents run as %s without the OS sandbox", os.environ.get("USER"))
        if self.args.chat:
            r = subprocess.run([sys.executable, str(self.rig / "chat" / "token_refresh.py"), "ensure"],
                               env=self.env, capture_output=True, text=True)
            msg = (r.stdout + r.stderr).strip().splitlines()
            if r.returncode:
                sys.exit(f"chat token check failed: {msg[-1] if msg else r.returncode} (see chat/README.md)")
            log.info("chat token: %s", msg[-1] if msg else "ok")

    def run(self):
        self.preflight()
        pid_file = self.log_dir / "supervisor.pid"
        if pid_file.exists():
            try:
                os.kill(int(pid_file.read_text()), 0)
                sys.exit(f"supervisor already running (pid {pid_file.read_text().strip()})")
            except (ValueError, ProcessLookupError, PermissionError):
                pass
        pid_file.write_text(str(os.getpid()))
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: self.stop.set())
        threads = [threading.Thread(target=self.status_loop, daemon=True),
                   threading.Thread(target=self.stream_loop, daemon=True)]
        if self.args.chat:
            threads.append(threading.Thread(target=self.chat_loop, daemon=True))
        log.info("supervisor started: stream=%s chat=%s player model=%s", self.args.stream, self.args.chat,
                 self.cfg["PLAYER_MODEL"])
        try:
            if not self.ensure_game():
                log.warning("game not ready yet; the play loop keeps retrying")
            self.release_stale_control()
            for t in threads:
                t.start()
            self.play_loop()
        finally:
            self.stop.set()
            with self.lock:
                player, chat, stream = self.player_proc, self.chat_proc, self.stream_proc
            self.terminate(player, group=True)
            self.terminate(chat, group=True)
            self.terminate(stream, signal.SIGINT, grace=15)
            for t in threads:
                t.join(20)
            try:
                self.write_status(inspect=False, mode="offline")
            except Exception:  # noqa: BLE001
                pass
            pid_file.unlink(missing_ok=True)
            if self.args.down:
                self.run_script("down.sh")
            log.info("supervisor stopped")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--stream", default="none", help="none | file:PATH | live")
    p.add_argument("--i-mean-it", action="store_true", help="required with --stream live")
    p.add_argument("--chat", action="store_true", help="also run the Twitch chat agent")
    p.add_argument("--max-games", type=int, default=0, help="stop after N matches (0 = run until stopped)")
    p.add_argument("--game-timeout", type=int, default=120, help="minutes before a player session is ended")
    p.add_argument("--down", action="store_true", help="run down.sh on exit")
    args = parser.parse_args()
    if not (args.stream in ("none", "live") or (args.stream.startswith("file:") and len(args.stream) > 5)):
        parser.error("--stream must be none, file:PATH or live")
    if args.stream == "live" and not args.i_mean_it:
        parser.error("refusing to go live without --i-mean-it (and the user's explicit go-ahead)")
    cfg = rigconfig.load()
    pathlib.Path(cfg["LOG_DIR"]).mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(pathlib.Path(cfg["LOG_DIR"]) / "supervisor.log",
                                                   maxBytes=5 * 1024 * 1024, backupCount=3)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[handler, logging.StreamHandler()])
    Supervisor(args).run()


if __name__ == "__main__":
    main()
