// SPDX-License-Identifier: GPL-3.0-or-later
// Standing order installed by the trailer editor (an AI agent) through the game's
// MCP server (hive_program install) for the desktop trailer's co-play beat.
//
// Each run (every interval_ticks) lays the next building site of a short plan.
// PLAN lists a building family and an anchor tile in the filmed view; the run reads
// the colony's own view of the ground around the anchor (map.region: explored and
// visible tiles, no resource, no building, grass on every corner), picks
// the free footprint nearest the anchor that keeps one tile clear of the sites this
// order already laid, and orders one construction site there. capture_shot.py fills
// PLAN in from the shot's data. Only the player's fog-filtered view and ordinary
// player orders are used.
const PLAN = __PLAN__;
const NONE = 65535;
const GRASS = 2;   // terrain id of grass, the buildable ground (the release's local Hive has no terrainTypes())
let next = 0;
const placed = [];
function step(ctx) {
  if (next >= PLAN.length) return {output: {done: placed}};
  const g = ctx.game;
  const p = PLAN[next++];
  const type = g.buildingTypes().find(t => t.placeable && t.site && t.level === 0 &&
                                         String(t.name).toLowerCase() === p.type);
  if (!type) return {output: {missing_type: p.type}};
  const r = p.radius || 7, W = g.map.width, H = g.map.height;
  const x0 = p.x - r, y0 = p.y - r, size = 2 * r + type.width;
  const tiles = g.map.region(x0, y0, size, size);
  const free = tiles.map(t => t.explored && t.visible && t.resource && t.resource.type === NONE &&
    (t.building === undefined || t.building === NONE) && t.corners &&
    t.corners.every(c => c === GRASS));
  const wrap = (a, n) => { const d = Math.abs(a) % n; return Math.min(d, n - d); };
  let best = null, bestD = 1e9;
  for (let dy = 0; dy + type.height <= size; dy++) {
    for (let dx = 0; dx + type.width <= size; dx++) {
      let ok = true;
      for (let j = 0; j < type.height && ok; j++)
        for (let i = 0; i < type.width && ok; i++) ok = free[(dy + j) * size + dx + i];
      if (!ok) continue;
      const x = ((x0 + dx) % W + W) % W, y = ((y0 + dy) % H + H) % H;
      if (placed.some(q => wrap(q[0] - x, W) <= type.width && wrap(q[1] - y, H) <= type.height)) continue;
      const d = wrap(x - p.x, W) + wrap(y - p.y, H);
      if (d < bestD) { bestD = d; best = [x, y]; }
    }
  }
  if (!best) return {output: {no_room_near: [p.x, p.y], step: next}};
  placed.push(best);
  return {
    output: {placing: p.type, at: best, step: next, of: PLAN.length},
    orders: [{type: 'create', buildingType: type.id, x: best[0], y: best[1],
              workers: p.workers || 6, futureWorkers: p.workers || 6}],
  };
}
