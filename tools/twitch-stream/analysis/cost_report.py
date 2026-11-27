#!/usr/bin/env python3
"""Estimate what the stream's models cost, from real token usage since a cutoff.

  analysis/cost_report.py "2026-11-24 21:00"     (local time)

Reads the player transcripts modified since the cutoff and the chat host's decision log
($LOG_DIR/chat/agent.jsonl), and prices them at API list prices (PRICES, per million tokens;
update them when the model or prices change). The stream runs on a subscription, so this is
the API-equivalent cost, useful for comparing settings (pacing, compaction, prompts). Compare
runs per hour of stream, not per game: game lengths vary a lot. Compaction summaries aren't in
the call events, so this undercounts by roughly 15%; tool_usage.py --section coverage has the full
per-turn accounting, including compaction and killed turns.
"""
import argparse
import datetime
import json

import transcripts

# Sonnet 5.5 list prices, USD per million tokens (2026-11).
PRICES = {"input_tokens": 2.00, "output_tokens": 10.00, "cache_read_input_tokens": 0.10,
          "cache_write_5m": 2.50, "cache_write_1h": 4.00}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("since", help='local time, "YYYY-MM-DD HH:MM"')
    cut = datetime.datetime.strptime(ap.parse_args().since, "%Y-%m-%d %H:%M").timestamp()
    hours = (datetime.datetime.now().timestamp() - cut) / 3600
    tot = dict.fromkeys(PRICES, 0)
    n_calls = cli_cost = 0
    files = [p for p in transcripts.player_logs() if __import__("os").path.getmtime(p) >= cut]
    for path in files:
        for _, u in transcripts.calls(path):
            n_calls += 1
            for k in ("input_tokens", "cache_read_input_tokens"):
                tot[k] += u[k]
            tot["cache_write_1h"] += u["cache_write_1h"]
            tot["cache_write_5m"] += u["cache_creation_input_tokens"] - u["cache_write_1h"]
        # Streamed call events carry only a partial output count; each turn's result has the real one.
        # In a resumed session total_cost_usd is cumulative over its turns, so take the last, not the sum.
        results = [e for e in transcripts.events(path) if e.get("type") == "result"]
        tot["output_tokens"] += sum((e.get("usage") or {}).get("output_tokens", 0) or 0 for e in results)
        cli_cost += max([e.get("total_cost_usd") or 0 for e in results] or [0])
    cost = {k: tot[k] / 1e6 * PRICES[k] for k in PRICES}
    player = sum(cost.values())

    chat = chat_n = 0
    try:
        with open(transcripts.log_dir() / "chat" / "agent.jsonl") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    t = datetime.datetime.fromisoformat(d.get("at", "1970-01-01T00:00:00+00:00")).timestamp()
                except (ValueError, TypeError):
                    continue
                if t >= cut and d.get("cost_usd"):
                    chat += d["cost_usd"]
                    chat_n += 1
    except OSError:
        pass

    print(f"window: {hours:.2f} h, {len(files)} transcripts, {n_calls} player model calls ({n_calls / hours / 60:.1f}/min)")
    print("player tokens: " + ", ".join(f"{k} {v:,}" for k, v in tot.items()))
    for k, v in cost.items():
        print(f"  {k:24s} ${v:8.2f}")
    print(f"player total ${player:.2f} -> ${player / hours:.2f}/h, ${player / hours * 24:.0f}/day, "
          f"${player / hours * 24 * 30:.0f}/30 days")
    print(f"CLI-reported player cost (finished turns only, so partial) ${cli_cost:.2f}")
    print(f"chat host: {chat_n} replies, ${chat:.2f} -> ${chat / hours:.2f}/h")


if __name__ == "__main__":
    main()
