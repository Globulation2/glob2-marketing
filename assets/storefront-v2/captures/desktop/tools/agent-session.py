#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""A recorded MCP agent session for the AI co-play captures.

Every tool call this script makes to the game's built-in MCP server is appended,
request and response, to a JSON Lines transcript, so the terminal panel of the
side-by-side image can be rendered from calls that really happened, in order.

usage:
  agent-session.py TRANSCRIPT.jsonl call TOOL '{"json": "args"}'   one call (token added if "token" is "")
  agent-session.py TRANSCRIPT.jsonl install-frontline              the co-play standing order (below)

The standing order installed by `install-frontline` is small and real: every
150 ticks it looks at the enemy warriors the colony can see, finds the one
nearest to the colony's buildings, and keeps one war flag (radius 6, 12
warriors) on that tile, moving the flag when the enemy moves. It only uses the
player's own fog-filtered view (Hive API) and ordinary player orders.
"""
import json
import os
import sys
import time

import mcp

mcp.PORT = int(os.environ.get("GLOB2_MCP_PORT", "47815"))

FRONTLINE = r"""
// Frontline flag: keep one war flag on the visible enemy warrior nearest our buildings.
let flag = null, placedAt = null, waited = 0;
function step(ctx) {
  const g = ctx.game;
  const mine = g.buildings({team: ctx.myTeam}).filter(b => !b.virtual);
  if (!mine.length) return {output: {note: 'no buildings'}};
  const enemies = g.units({}).filter(u => u.team !== ctx.myTeam && u.type === 2);
  if (!enemies.length) return {output: {note: 'no enemy warriors in sight'}};
  const W = g.map.width, H = g.map.height;
  const wrap = (a, n) => { const d = Math.abs(a) % n; return Math.min(d, n - d); };
  let best = null, bestD = 1e9;
  for (const e of enemies) {
    for (const b of mine) {
      const d = wrap(e.x - b.x, W) + wrap(e.y - b.y, H);
      if (d < bestD) { bestD = d; best = e; }
    }
  }
  let current = flag ? g.building(flag) : null;
  if (!current && placedAt) {
    // adopt the flag this program placed on its previous run
    const f = g.buildings({team: ctx.myTeam}).find(b => b.virtual && b.shortType === 9 &&
      wrap(b.x - placedAt[0], W) + wrap(b.y - placedAt[1], H) <= 1);
    if (f) { flag = {id: f.id, generation: f.generation}; current = f; }
    else if (++waited < 3) return {output: {waiting_for_flag: placedAt}};
  }
  if (!current) {
    const type = g.buildingTypes().find(t => t.name === 'warflag' && t.virtual);
    flag = null; placedAt = [best.x, best.y]; waited = 0;
    return {output: {placed: [best.x, best.y], enemies: enemies.length},
            orders: [{type: 'create', buildingType: type.id, x: best.x, y: best.y,
                      workers: 12, futureWorkers: 12, range: 6}]};
  }
  if (wrap(current.x - best.x, W) + wrap(current.y - best.y, H) > 3) {
    return {output: {moved: [best.x, best.y], enemies: enemies.length},
            orders: [{type: 'moveFlag', building: current, x: best.x, y: best.y}]};
  }
  return {output: {holding: [current.x, current.y], enemies: enemies.length}};
}
"""


def record(path, tool, args, data, err, started):
    with open(path, "a") as fh:
        fh.write(json.dumps({"t": round(started, 3), "tool": tool,
                             "arguments": {k: ("<token>" if k == "token" else v) for k, v in args.items()},
                             "is_error": err, "result": data}) + "\n")


def call(path, tool, args):
    args = dict(args)
    if args.get("token") == "":
        args["token"] = mcp.token()
    started = time.time()
    data, images, err = mcp.call(tool, args)
    if images:
        data = {"_images": len(images), "data": data}
    record(path, tool, args, data, err, started)
    return data, err


def main(argv):
    path, cmd = argv[0], argv[1]
    if cmd == "call":
        data, err = call(path, argv[2], json.loads(argv[3]) if len(argv) > 3 else {})
        print(json.dumps(data, indent=1)[:4000])
        return 1 if err else 0
    if cmd == "install-frontline":
        status, _ = call(path, "hive_status", {})
        data, err = call(path, "hive_program", {
            "action": "install", "token": "", "session": status["session"],
            "operation_key": f"frontline-{int(time.time())}", "name": "frontline-flag",
            "description": "Keep one war flag on the enemy warrior nearest our buildings",
            "source": FRONTLINE, "interval_ticks": 150})
        print(json.dumps(data, indent=1)[:4000])
        return 1 if err else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
