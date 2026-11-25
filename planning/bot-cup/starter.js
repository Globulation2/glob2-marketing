// SPDX-License-Identifier: GPL-3.0-only
// Adapted from the Globulation 2 Readable Colony starter. See LICENSE.

// src/economy.js
var pending = null;
var nextBuild = 0;
var zoned = false;
// BOT CUP EXERCISE
// Predict what will happen if the colony aims for at least three inns.
// Change 2 to 3, save a copy, and compare both bots on the same map.
var MINIMUM_INNS = 2;
function economy(ctx, buildings, units, home, planConstruction) {
  const inns = buildings.filter((b) => b.shortType === 1);
  // Grow the inn target as the population grows, keeping at least the minimum.
  const wantedInns = Math.max(MINIMUM_INNS, Math.ceil(units.length / 10));
  for (const b of buildings) {
    if (b.virtual) continue;
    const workers = b.construction ? 3 : b.shortType === 0 ? 1 : b.shortType === 1 ? 5 : 2;
    if (b.workers !== workers) b.workers = workers;
    b.priority = b.shortType === 1 ? 1 : 0;
    if (b.shortType === 0) {
      const ratios = inns.length < wantedInns ? [4, 1, 0] : units.length < 24 ? [6, 1, 1] : [5, 1, 3];
      if (b.production.some((v, i) => v !== ratios[i])) b.production = ratios;
    }
  }
  ctx.telemetry.set("economy.foodCapacityTarget", wantedInns, { unit: "inns" });
  if (pending !== null) {
    const status = ctx.actions.status(pending);
    if (status && ["pending", "issued", "constructing"].includes(status.status))
      return;
    ctx.telemetry.set(
      "construction.lastResult",
      status ? status.status : "expired"
    );
    pending = null;
  }
  if (!planConstruction || ctx.tick < nextBuild) return;
  nextBuild = ctx.tick + 512;
  let family = null;
  if (inns.length < wantedInns) family = "inn";
  else {
    const progression = [
      ["racetrack", 3],
      // Swimming lets workers harvest algae needed by schools.
      ["swimmingpool", 4],
      ["school", 6],
      ["barracks", 5],
      ["hospital", 2]
    ];
    for (const [name, id] of progression)
      if (!buildings.some((b) => b.shortType === id)) {
        family = /** @type {import('../types/glob2').BuildingName} */
        name;
        break;
      }
    if (!family && units.length > 55 && buildings.filter((b) => b.shortType === 0).length < 2)
      family = "swarm";
  }
  if (!family) return;
  const region = {
    x: home.x - 28,
    y: home.y - 28,
    width: Math.min(56, ctx.game.map.width),
    height: Math.min(56, ctx.game.map.height)
  };
  const request = {
    building: family,
    region,
    anchor: { x: home.x, y: home.y },
    reserveUpgrade: true,
    workers: 3,
    futureWorkers: 3,
    constraints: [
      {
        metric: "distance",
        sources: { resource: "wheat" },
        distanceMetric: "chebyshev",
        max: family === "inn" ? 14 : 28
      }
    ],
    preferences: [
      {
        metric: "distance",
        sources: { points: [{ x: home.x, y: home.y }] },
        distanceMetric: "chebyshev",
        weight: -2
      },
      { metric: "resourceDensity", resource: "wheat", radius: 8, weight: 3 },
      { metric: "fertility", radius: 4, weight: 1 }
    ]
  };
  pending = ctx.actions.build(
    /** @type {import('../types/glob2-v2').Placement} */
    request
  );
  ctx.telemetry.set("construction.planned", family);
  ctx.telemetry.set("construction.foundSite", pending !== null);
  if (!zoned) {
    ctx.actions.zone({
      type: "guardArea",
      x: home.x,
      y: home.y,
      width: 3,
      height: 3,
      mode: 1,
      mask: [true, true, true, true, true, true, true, true, true]
    });
    zoned = true;
    ctx.telemetry.set("colony.guardZone", true);
  }
}

// src/technology.js
var pending2 = null;
var clearing = null;
function technology(ctx, buildings) {
  const workers = ctx.game.units({ team: ctx.myTeam, limit: 512 }).filter((u) => u.type === 0);
  const trainedFor = (level) => workers.filter((u) => u.levels[6] > level).length >= 5;
  ctx.telemetry.set(
    "technology.trainedWorkers",
    workers.filter((u) => u.levels[6] > 0).length
  );
  ctx.telemetry.set(
    "technology.upgradedBuildings",
    buildings.filter((b) => !b.construction && b.level > 0).length
  );
  const clearFlag = buildings.find((b) => b.shortType === 10);
  if (pending2 !== null) {
    const status = ctx.actions.status(pending2);
    ctx.telemetry.set(
      "technology.actionStatus",
      status ? status.status : "expired"
    );
    if (status && status.reason)
      ctx.telemetry.set("technology.actionReason", status.reason);
    if (status && ["pending", "issued", "constructing"].includes(status.status)) {
      if (clearFlag && status.status === "constructing") clearFlag.workers = 0;
      return;
    }
    pending2 = null;
  }
  const damaged = buildings.find(
    (b) => !b.virtual && !b.construction && b.hp < b.maxHp * 0.7
  );
  if (damaged) {
    pending2 = ctx.actions.repair({
      building: damaged.ref,
      workers: 3,
      futureWorkers: 2
    });
    return;
  }
  const schools = buildings.filter((b) => b.shortType === 6 && !b.construction);
  const candidate = schools.find((b) => b.level < 2 && trainedFor(b.level)) || schools.length && buildings.find(
    (b) => !b.virtual && !b.construction && b.level < 2 && trainedFor(b.level) && [1, 3, 4, 5].includes(b.shortType)
  );
  if (candidate) {
    const variant = ctx.game.buildingTypes().find((t) => t.id === candidate.type);
    const x = (candidate.x + Math.floor(variant.width / 2)) % ctx.game.map.width;
    const y = (candidate.y + Math.floor(variant.height / 2)) % ctx.game.map.height;
    if (clearFlag) {
      clearFlag.x = x;
      clearFlag.y = y;
      clearFlag.range = 4;
      clearFlag.workers = 3;
      clearFlag.clearingResources = [true, true, true, false, true];
    } else if (clearing === null || !["pending", "issued"].includes(
      ctx.actions.status(clearing)?.status || ""
    )) {
      clearing = ctx.actions.build({
        building: "clearingflag",
        region: { x, y, width: 1, height: 1 },
        workers: 3,
        range: 4
      });
    }
    pending2 = ctx.actions.upgrade({
      building: candidate.ref,
      workers: 3,
      futureWorkers: 2
    });
    ctx.telemetry.set("technology.upgradeFamily", candidate.shortType);
  }
}

// src/military.js
var exploration = null;
var attack = null;
var direction = 0;
function military(ctx, buildings, units, home) {
  const explorer = buildings.find((b) => b.shortType === 8);
  const war = buildings.find((b) => b.shortType === 9);
  const warriors = units.filter((u) => u.type === 2).length;
  const hotspots = ctx.spatial.hotspots({
    sources: {
      units: { relation: "enemy", type: "warrior" },
      weight: "strength"
    },
    radius: 6,
    limit: 3
  });
  ctx.telemetry.set(
    "military.visibleThreat",
    hotspots.length ? hotspots[0].score : 0
  );
  const enemies = ctx.game.buildings({ limit: 256 }).filter(
    (b) => b.team !== ctx.myTeam && !(ctx.game.teams().find((t) => t.id === ctx.myTeam).allies & 1 << b.team)
  );
  const target = enemies[0] || hotspots[0];
  if (target && warriors >= 6) {
    ctx.telemetry.set("military.attacking", true);
    if (war) {
      war.x = target.x;
      war.y = target.y;
      war.workers = Math.min(20, warriors);
      war.range = 8;
    } else if (!active(ctx, attack))
      attack = ctx.actions.build({
        building: "warflag",
        region: { x: target.x, y: target.y, width: 1, height: 1 },
        workers: Math.min(20, warriors),
        range: 8
      });
  }
  if (explorer) {
    ctx.telemetry.set("military.exploring", true);
    const cell = direction++ % 64;
    explorer.x = (home.x + (cell % 8 - 3) * Math.ceil(ctx.game.map.width / 8) + ctx.game.map.width) % ctx.game.map.width;
    explorer.y = (home.y + (Math.floor(cell / 8) - 3) * Math.ceil(ctx.game.map.height / 8) + ctx.game.map.height) % ctx.game.map.height;
    explorer.workers = 2;
    explorer.range = 12;
  } else if (!active(ctx, exploration)) {
    const type = ctx.game.buildingTypes().find((t) => t.name === "explorationflag");
    if (type)
      exploration = ctx.actions.create({
        buildingType: type.id,
        x: home.x,
        y: home.y,
        workers: 2,
        futureWorkers: 2,
        range: 12
      });
  }
  ctx.telemetry.set("military.warriors", warriors, { unit: "units" });
}
function active(ctx, id) {
  if (id === null) return false;
  const status = ctx.actions.status(id);
  return !!status && ["pending", "issued", "constructing"].includes(status.status);
}

// src/index.js
var nextDecision = 0;
var decisions = 0;
function metadata() {
  return {
    apiVersion: 2,
    name: "Bot Cup Starter",
    description: "A commented, complete starter AI: food, technology, exploration and attacks.",
    version: "1.0.0",
    author: "Globulation2"
  };
}
function step(ctx) {
  if (ctx.tick < nextDecision) return;
  nextDecision = ctx.tick + 128;
  decisions++;
  const buildings = ctx.game.buildings({ team: ctx.myTeam, limit: 128 });
  const units = ctx.game.units({ team: ctx.myTeam, limit: 512 });
  const home = buildings.find((b) => b.shortType === 0 && !b.construction) || buildings.find((b) => !b.virtual);
  if (!home) return;
  economy(ctx, buildings, units, home, decisions % 4 === 1);
  if (decisions % 4 === 0) technology(ctx, buildings);
  if (decisions % 4 === 2) military(ctx, buildings, units, home);
  ctx.telemetry.set(
    "strategy.phase",
    units.length < 30 ? "establishment" : "expansion"
  );
  ctx.telemetry.set("strategy.decisions", decisions);
  ctx.telemetry.set("colony.population", units.length, {
    unit: "units",
    description: "Own units in the bounded scan"
  });
}
export {
  metadata,
  step
};
