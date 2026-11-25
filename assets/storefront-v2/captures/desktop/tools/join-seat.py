#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Add a local human player to one colony of a headless Globulation 2 save.

`glob2 game run` writes saves whose seats are all AI players, so the game opens
them in spectator view. The game gives the camera a real player seat (normal
HUD, fog of war, build menu, building panels) when the save's header holds a
local player (Engine::finishGameInit). Globulation 2 lets several players
control one colony, so this tool adds one more player record:

  * game header: numberOfPlayers + 1, and the first unused player slot becomes a
    local player on the chosen team (its default 12-byte name "Debug Player" is
    replaced by a 12-byte name, so no header offset moves);
  * the chosen team's two BaseTeam records (map header and game body):
    numberOfPlayer + 1 and the new player's bit in playersMask;
  * game body: one new "PLYb … PLYe" Player record after the last one.

Nothing else changes: map, units, buildings, resources and every AI's state are
byte-identical, and the colony's AI keeps playing it. The local player shares
that colony, exactly as a second human on the same team would.

Optional --rename OLD=NEW renames players (same byte length only), e.g. the
headless runner's lowercase "maxima" to the lobby's "Maxima".

usage: join-seat.py IN.game.gz OUT.game.gz TEAM [--name TWELVE_BYTES] [--rename OLD=NEW ...]
"""
import argparse
import gzip
import struct
import sys

P_LOCAL = 4
P_AI = 5
DEFAULT_NAME = b"Debug Player"


def u32(data, pos):
    return struct.unpack(">I", data[pos:pos + 4])[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("team", type=int)
    ap.add_argument("--name", default="Local Player", help="12-byte name of the added player")
    ap.add_argument("--rename", action="append", default=[], metavar="OLD=NEW")
    args = ap.parse_args()
    name = args.name.encode()
    if len(name) != len(DEFAULT_NAME):
        raise SystemExit("--name must be exactly 12 bytes")

    data = bytearray(gzip.open(args.src, "rb").read())
    team = args.team

    # --- locate the game header's player table: numberOfPlayers then player 0
    first = data.find(b"PLYb")
    if first < 0:
        raise SystemExit("no Player records")
    # body player records give the authoritative list
    players = []  # (offset, type, number, name, team)
    pos = first
    while data[pos:pos + 4] == b"PLYb":
        ptype, number, mask, _pid, nlen = struct.unpack(">IiIII", data[pos + 4:pos + 24])
        pname = bytes(data[pos + 24:pos + 24 + nlen])
        pteam, _tmask, sx, sy = struct.unpack(">iIii", data[pos + 24 + nlen:pos + 40 + nlen])
        end = data.find(b"PLYe", pos + 40 + nlen)
        if ptype >= P_AI:
            end = data.find(b"AI ePLYe", pos) + 4
        players.append(dict(pos=pos, type=ptype, number=number, name=pname, team=pteam, start=(sx, sy)))
        pos = end + 4
    after_players = pos
    n = len(players)
    owners = [p for p in players if p["team"] == team]
    if not owners:
        raise SystemExit(f"no player controls team {team}")
    owner = owners[0]

    # header: numberOfPlayers(u32) followed by player 0's record
    p0 = players[0]
    key = struct.pack(">I", n) + struct.pack(">IiI", p0["type"], 0, 1)
    hpos = data.find(key, 0, first)
    if hpos < 0 or data.find(key, hpos + 1, 8192) >= 0:
        raise SystemExit("cannot locate the header player table")
    # walk to slot n
    slot = hpos + 4
    for _ in range(n):
        nlen = u32(data, slot + 16)
        slot += 20 + nlen + 8
    if u32(data, slot) != 0 or bytes(data[slot + 20:slot + 32]) != DEFAULT_NAME:
        raise SystemExit("unexpected layout of the first unused player slot")
    data[hpos:hpos + 4] = struct.pack(">I", n + 1)
    data[slot:slot + 40] = (struct.pack(">IiII", P_LOCAL, n, 1 << n, 0) + struct.pack(">I", 12) + name
                            + struct.pack(">iI", team, 1 << team))

    # --- BaseTeam records: [type][teamNumber][numberOfPlayer][r g b a][playersMask]
    # The map header ends with one 20-byte record per team, directly before the
    # game header (8 bytes of rates, then numberOfPlayers at hpos); the game
    # body repeats the same record at the start of that team's data.
    mask = 0
    for p in owners:
        mask |= 1 << p["number"]
    teams = max(p["team"] for p in players) + 1
    while True:  # walk back over team records to find how many the header holds
        rec = hpos - 8 - 20 * (teams + 1)
        if rec < 0 or struct.unpack(">i", data[rec + 4:rec + 8])[0] != 0 or teams >= 32:
            break
        teams += 1
    first_team = hpos - 8 - 20 * teams
    if struct.unpack(">i", data[first_team + 4:first_team + 8])[0] != 0:
        raise SystemExit("cannot locate the header team table")
    rec = first_team + 20 * team
    old = bytes(data[rec:rec + 20])
    if struct.unpack(">iiI", old[4:12] + old[16:20]) != (team, len(owners), mask):
        raise SystemExit(f"unexpected header BaseTeam record for team {team}")
    new = old[:8] + struct.pack(">i", len(owners) + 1) + old[12:16] + struct.pack(">I", mask | (1 << n))
    body = data.find(old, hpos)
    if body < 0 or body > first or data.find(old, body + 1, first) >= 0:
        raise SystemExit(f"cannot locate the body BaseTeam record for team {team}")
    data[rec:rec + 20] = new
    data[body:body + 20] = new

    # --- body: insert the new Player record after the last one
    record = (b"PLYb" + struct.pack(">IiII", P_LOCAL, n, 1 << n, 0) + struct.pack(">I", 12) + name
              + struct.pack(">iIii", team, 1 << team, *owner["start"]) + b"PLYe")
    data[after_players:after_players] = record

    for spec in args.rename:
        old, new = (s.encode() for s in spec.split("=", 1))
        if len(old) != len(new):
            raise SystemExit(f"rename {spec}: lengths differ")
        needle = struct.pack(">I", len(old)) + old
        count = pos = 0
        while True:
            pos = data.find(needle, pos)
            if pos < 0:
                break
            t, m = struct.unpack(">iI", data[pos + len(needle):pos + len(needle) + 8])
            if 0 <= t < 32 and m == (1 << t):  # only BasePlayer names
                data[pos + 4:pos + 4 + len(old)] = new
                count += 1
            pos += 1
        print(f"renamed {old.decode()} -> {new.decode()} in {count} records", file=sys.stderr)

    with gzip.open(args.dst, "wb", compresslevel=6) as fh:
        fh.write(bytes(data))
    print(f"player {n} ({args.name}) joined team {team} alongside {owner['name'].decode()}: {args.dst}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
