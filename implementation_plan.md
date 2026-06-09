# Implementation Plan — Wolff Flagship Fund Integration & Parallel Simulation

We will implement a parallel simulation of Peter Wolff's Flagship Fund copy-trading strategy alongside your live catalyst-based strategy. The simulation will run locally in memory as a completely separate virtual account starting with **$1,000 in virtual cash** and 0 holdings.

Additionally, we will integrate Wolff's stock holdings and accumulation zone alerts as research signals to influence the opportunity scores of your live trading agent.

---

## User Review Required

> [!IMPORTANT]
> **No live trades will be placed for the Wolff strategy.** The Wolff Copy-Trader will run strictly as a local simulation for 1–2 weeks. You can inspect its simulated trades, portfolio breakdown, and performance in your daily Telegram reports before deciding whether to enable it for real execution.

> [!TIP]
> **Signal Integration is active**: The subagents will immediately begin scanning Peter Wolff's public Substack and X posts. If a stock on your live agent's watchlist is also recommended or held by Wolff, it will receive a boost in its decision score, helping align your live picks with his research.

---

## Proposed Changes

### 1. Configuration Settings
We will update `config/agent_config.json` to define the Wolff strategy simulation settings and the signal boost weight.

#### [MODIFY] [agent_config.json](file:///C:/Projects/Trad/config/agent_config.json)
```json
{
  "mode": "live",
  "account_number": "514240167",
  "telegram": {
    "bot_token": "8921546887:AAECsdY6ipILmHYV5MOT9jaaEetUQykX9GQ",
    "chat_id": "536039236"
  },
  "risk_rules": {
    "max_position_pct": 18,
    "max_positions": 5,
    "min_positions": 2,
    "hard_stop_loss_pct": 8,
    "take_profit_trigger_pct": 10,
    "trailing_stop_pct": 5,
    "cash_reserve_pct": 10,
    "max_daily_trades": 3,
    "min_stock_price": 5.00
  },
  "exclusions": {
    "categories": ["penny_stocks", "chinese_adrs", "meme_stocks"],
    "blocked_symbols": [
      "GME", "AMC", "BBBY", "KOSS", "BB", "CLOV", "WISH", "WKHS",
      "BABA", "PDD", "JD", "NIO", "XPEV", "LI", "BIDU", "BILI", "IQ", "TAL", "FUTU", "TME", "DIDI",
      "TCEHY", "BEKE", "ZH", "YMM", "MNSO", "GDS", "KC", "VNET", "QFIN", "TIGR", "FINV"
    ]
  },
  "wolff_simulation": {
    "enabled": true,
    "starting_capital": 1000.00,
    "cash_reserve_pct": 10.0,
    "max_position_pct": 18.0,
    "signal_score_boost": 1.5,
    "description": "Runs a parallel, simulated copy of Wolff's Flagship Fund starting with $1,000 cash. No real orders are submitted for this strategy."
  },
  "schedule": {
    "cron_utc": "0 14 * * 1-5"
  }
}
```

---

### 2. Strategy and Prompts Update
We will update `.gemini/skills/daily_fa/SKILL.md` to incorporate Wolff's research into the workflow.

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)
*   **Phase 1 (Research)**: Update **Sub-Agent B (Fundamental & Macro Analyst)** to search Wolff's Substack (`wolff.substack.com`) and X account for recent "Flagship Report" updates, compiling his current holdings, target weights, and accumulation zones.
*   **Phase 2B (Opportunity Scoring)**: If a candidate stock evaluated by the live engine is currently held or flagged as a "buy" in Wolff's latest report, add a **+1.5 point boost** to its portfolio fit score (Step 2B).
*   **Phase 3.5 (Wolff Portfolio Simulation - Parallel Engine)**:
    1. Check `memory/wolff_journal.json`. If it does not exist, initialize a virtual portfolio with **$1,000 in virtual cash** and 0 positions.
    2. For any virtual holdings currently in the portfolio, call `get_equity_quotes` via the Robinhood MCP to get their actual, current prices.
    3. Calculate the total current virtual portfolio value (simulated cash + current value of virtual positions).
    4. Compare current virtual allocations to Wolff's target weights.
    5. Calculate the required virtual transactions (trims/sells first, then buys) while keeping a 10% simulated cash reserve.
    6. Save these simulated trades in `memory/wolff_trades.json` and update `memory/wolff_journal.json` with the new share quantities, average buy prices, and cash balance.
*   **Phase 4 (Reporting)**: Append a **Wolff Flagship Simulation** card in the HTML report and a summary section in the Telegram message displaying the simulated portfolio's composition, P&L, and pending rebalances.

---

### 3. New Memory Files
We will create separate memory files to track the state of the simulated Wolff portfolio.

#### [NEW] [wolff_journal.json](file:///C:/Projects/Trad/memory/wolff_journal.json)
Tracks the daily asset allocation and rolling 7-day state of the simulated Wolff portfolio.
```json
{
  "entries": [
    {
      "date": "2026-06-09",
      "simulated_cash": 1000.00,
      "total_portfolio_value": 1000.00,
      "positions": [],
      "rebalance_decisions": []
    }
  ]
}
```

#### [NEW] [wolff_trades.json](file:///C:/Projects/Trad/memory/wolff_trades.json)
Maintains the permanent transaction log of all simulated buy/sell orders executed for the Wolff copy-trading strategy.
```json
{
  "trades": [],
  "performance": {
    "total_trades": 0,
    "winning_trades": 0,
    "losing_trades": 0,
    "total_realized_pnl": 0.0,
    "win_rate_pct": 0.0
  }
}
```

---

## Verification Plan

### Automated Verification
1.  **Manual Dry Run**: Trigger a manual execution of the modified workflow in `"dry_run"` mode to verify:
    *   The research subagent successfully queries and parses Wolff's Substack.
    *   The live strategy candidate scoring logs show the `+1.5` score boost when matching his picks.
    *   The parallel rebalancing algorithm runs using the $1,000 virtual portfolio value.
    *   The simulated actions are written to `wolff_trades.json` and `wolff_journal.json` without placing orders.
    *   The Telegram and HTML reports contain the new Wolff sections.

### Manual Verification
*   **Review Telegram Message**: Verify that the daily Telegram report includes the new "Wolff Flagship Fund Simulation" summary card.
*   **Inspect HTML Report**: Open `reports/daily_report.html` to confirm that the Wolff portfolio table displays correctly alongside the live portfolio.
*   **Audit memory files**: Review `wolff_journal.json` and `wolff_trades.json` to verify simulated positions are tracked accurately over multiple runs.
