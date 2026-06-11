import json
import os

MEMORY_DIR = r"C:\Projects\Trad\memory"
journal_path = os.path.join(MEMORY_DIR, "journal.json")

with open(journal_path, "r", encoding="utf-8") as f:
    journal = json.load(f)

new_entry = {
  "date": "2026-06-11",
  "type": "daily_run",
  "macro_regime": "cautious",
  "vix": 22.22,
  "spx_vs_ma": "above",
  "market_conditions": "📈 Futures rebounding (Nasdaq +1.22%, SPX +0.76%) after hot May PPI (+6.5% YoY) print. Oil premium persists due to US-Iran tensions. Fed is in blackout.",
  "portfolio_snapshot": {
    "total_value": 494.65,
    "cash_available": 74.40,
    "positions_count": 4,
    "positions": [
      {"symbol": "LLY", "qty": 0.12951, "avg_price": 1158.21, "current_price": 1142.33, "pnl_pct": -1.37},
      {"symbol": "RTX", "qty": 0.833263, "avg_price": 180.02, "current_price": 180.04, "pnl_pct": 0.01},
      {"symbol": "DVN", "qty": 1.938345, "avg_price": 46.06, "current_price": 46.51, "pnl_pct": 0.98},
      {"symbol": "MSFT", "qty": 0.08182, "avg_price": 404.30, "current_price": 392.71, "pnl_pct": -2.87}
    ]
  },
  "news_catalysts": [
    "BofA double upgrades Intel (INTC) to Buy, raising PT to $135.",
    "Lovesac (LOVE) beats Q1 EPS expectations (-$0.76 vs -$0.97).",
    "Fitch warns on deteriorating sovereign outlook due to Middle East tensions.",
    "Oracle (ORCL) double beat yesterday but sold off 8% on high capex concerns."
  ],
  "decisions": [
    {"action": "HOLD", "symbol": "LLY", "reason": "No news, within risk limits."},
    {"action": "HOLD", "symbol": "RTX", "reason": "Defense sector tailwinds intact."},
    {"action": "HOLD", "symbol": "DVN", "reason": "Oil price support due to geopolitical tensions."},
    {"action": "HOLD", "symbol": "MSFT", "reason": "Wolff Flagship pick, within limits."}
  ],
  "orders_placed": [],
  "signal_modifiers_applied": [
    {"symbol": "MSFT", "boost": 1.5, "reason": "Wolff Flagship Report"}
  ],
  "trailing_stop_peaks": {},
  "reasoning": "Regime remains Cautious (VIX 22.22). No cash available above the 15% reserve limit (held $74.40 cash vs $74.17 reserve target). The highest scoring new candidates were INTC (Score 7.0) and LOVE (Score 7.0 after +1.0 earnings beat modifier). Since neither candidate scored >= 7.5, no portfolio rotation was triggered. All current positions are held."
}

# Add entry
journal["entries"].append(new_entry)
if len(journal["entries"]) > 7:
    journal["entries"] = journal["entries"][-7:]

with open(journal_path, "w", encoding="utf-8") as f:
    json.dump(journal, f, indent=2)

print("Main journal updated!")
