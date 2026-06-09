# FA Agent — Phase 2 Intelligence Upgrade

Adding 4 new signal catalogs to the live scoring engine, a Macro Regime Classifier that controls risk settings daily, and a second parallel simulation (ARK Invest copy-trading) alongside the existing Wolff Flagship sim.

---

## Summary of Changes

| # | Feature | Where | Impact |
|---|---|---|---|
| 1 | Macro Regime Classifier | Phase 0 (Pre-Flight) | Dynamic risk settings |
| 2 | SEC Form 4 Insider Buys | Phase 1, Sub-Agent B | Score boost up to +1.0 |
| 3 | Earnings Calendar (EPS beats) | Phase 1, Sub-Agent A | Score boost up to +2.0 |
| 4 | Congress Trades (Quiver Quant) | Phase 1, Sub-Agent B | Score boost up to +1.0 |
| 5 | ARK Invest Simulation | Phase 3.5 (parallel) | New $1K virtual portfolio |

---

## Proposed Changes

### Component 1: `agent_config.json`

#### [MODIFY] [agent_config.json](file:///C:/Projects/Trad/config/agent_config.json)

Add two new top-level blocks:

1. **`macro_regime`**: defines thresholds for VIX and S&P 500 MA-based regime classification:
   - `risk_on`: VIX < 18 → normal rules
   - `cautious`: VIX 18–25 → cash_reserve 15%, min_score 6.5
   - `risk_off`: VIX > 25 → cash_reserve 25%, min_score 7.5, no new buys

2. **`ark_simulation`**: mirrors the `wolff_simulation` block:
   - `enabled: true`
   - `starting_capital: 1000.00`
   - `cash_reserve_pct: 10.0`
   - `max_position_pct: 18.0`
   - `signal_score_boost: 0.75` (smaller than Wolff — ARK is more speculative)
   - `source`: ARK daily disclosed trades at `https://ark-funds.com/funds/arkk/`

---

### Component 2: `SKILL.md` — Phase 0 (Pre-Flight)

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)

Add **Step 4: Macro Regime Classification** at the end of Phase 0:

- Agent fetches today's VIX value (from Sub-Agent B later, or cached from yesterday's journal)
- Agent checks if SPX is above or below its 50-day moving average (via news/finviz search)
- Classifies regime as `risk_on`, `cautious`, or `risk_off`
- Writes the regime into today's journal entry
- **Overrides** `cash_reserve_pct` and minimum buy score for the rest of the day's run:

| Regime | cash_reserve_pct | min_score | New buys allowed? |
|---|---|---|---|
| 🟢 risk_on | 10% (config default) | 6.0 | Yes |
| 🟡 cautious | 15% | 6.5 | Yes |
| 🔴 risk_off | 25% | 7.5 | No (unless rotation) |

---

### Component 3: `SKILL.md` — Phase 1 (Research Sub-Agents)

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)

**Sub-Agent A (News Feed Analyst)** gets a new section:

```
5. EARNINGS CALENDAR CHECK:
   - Search Yahoo Finance or EarningsWhispers for today's earnings releases.
   - For each company that ALREADY REPORTED today:
     - Did they beat EPS estimates? By how much?
     - Did they raise/lower guidance?
     - Beat + raised guidance = STRONG CATALYST (+2.0 to scoring)
     - Beat only = moderate catalyst (+1.0)
     - Miss = negative flag (mark for avoidance)
   - For companies reporting TOMORROW PRE-MARKET:
     - Flag them as "earnings risk" — do NOT initiate a new position today.
```

**Sub-Agent B (Fundamental & Macro Analyst)** gets two new sections:

```
6. SEC FORM 4 — INSIDER BUYING:
   - Search OpenInsider (openinsider.com) or SEC EDGAR for Form 4 filings in the last 48 hours.
   - Filter for: transaction_type = "Purchase" (P), amount > $50,000.
   - Cluster buys: 3+ insiders buying same company = STRONG signal.
   - Single large buy (>$500K) = MODERATE signal.
   - Ignore: "Automatic exercise of options" and "Disposition" transactions.
   - Return list of: company, insider title, dollar amount, date.

7. CONGRESS TRADES — STOCK ACT DISCLOSURES:
   - Search QuiverQuant (quiverquant.com/congresstrading) for congressional stock purchases in the last 7 days.
   - Focus on PURCHASES only (not sales or options).
   - Multiple Congress members buying same stock = stronger signal.
   - Return list of: ticker, Congress member, party, amount, date.
```

---

### Component 4: `SKILL.md` — Phase 2B (Scoring Engine)

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)

In Step 2D (Memory-Informed Adjustments), expand the score modifier table:

| Signal | Boost | Condition |
|---|---|---|
| Wolff Flagship holding/pick | +1.5 | Stock in Wolff's latest report |
| ARK Invest recent purchase | +0.75 | ARK bought in last 3 trading days |
| SEC Form 4 cluster buy | +1.0 | 3+ insiders buying in last 48h |
| SEC Form 4 single large buy | +0.5 | 1 insider >$500K in last 48h |
| Congress cluster buy | +1.0 | 3+ members bought in last 7 days |
| Congress single buy | +0.5 | 1 member bought in last 7 days |
| Earnings beat + raised guidance | +2.0 | Already reported today |
| Earnings beat only | +1.0 | Already reported today |
| Earnings miss | -2.0 | Already reported today |
| Earnings tomorrow (pre-market) | BLOCK | Do not initiate position today |

**Maximum cumulative boost per stock: +4.0** (to prevent outliers from bypassing score framework entirely)

---

### Component 5: `SKILL.md` — Phase 3.5 (ARK Simulation)

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)

Add a new **Phase 3.5b: ARK Invest Fund Simulation** block that mirrors the Wolff simulation logic:

1. **Source**: ARK discloses daily trade CSVs at `https://ark-funds.com/funds/arkk/` (ARKK only for now — their flagship)
2. **Initialize or Load**:
   - Read `memory/ark_journal.json`. If empty/missing, initialize with $1,000 starting capital and `positions: []`.
3. **Get ARK's Current Holdings**:
   - Scrape or fetch ARKK's disclosed portfolio. They publish a daily CSV with ticker, weight %, and shares held.
   - Parse the top 15 holdings by weight (capped at 18% per position per our rules).
4. **Rebalance Virtual Portfolio**:
   - Same delta-rebalancing logic as Wolff sim.
   - Use Robinhood `get_equity_quotes` to price virtual holdings.
5. **Log Trades**:
   - Append to `memory/ark_trades.json` with `"mode": "ark_simulation"`.

---

### Component 6: Memory Files (NEW)

#### [NEW] `memory/ark_journal.json`
Initialize with same structure as `wolff_journal.json`:
```json
{ "entries": [] }
```

#### [NEW] `memory/ark_trades.json`
Initialize with same structure as `wolff_trades.json`:
```json
{
  "trades": [],
  "performance": {
    "total_trades": 0, "winning_trades": 0,
    "losing_trades": 0, "total_realized_pnl": 0.0, "win_rate_pct": 0.0
  }
}
```

---

### Component 7: Reporting — Phase 4

#### [MODIFY] [SKILL.md](file:///C:/Projects/Trad/.gemini/skills/daily_fa/SKILL.md)

**Report 1 (Main)**: Add a new "Signal Intelligence" section to the HTML dashboard showing:
- Today's **Macro Regime** badge (🟢/🟡/🔴) with VIX value
- **Score modifier table**: which boosts were applied to which stocks and why
- Insider, Congress, and ARK signal alerts for any matched tickers

**Report 3 (NEW): ARK Simulation Report**
- Identical structure to the Wolff simulation report
- Saved to: `C:\Projects\Trad\reports\ark_simulation_report.html`
- Text summary to: `C:\Projects\Trad\scripts\ark_last_report.txt`
- Sent via Telegram as a 3rd report

---

## Verification Plan

### Automated
- Run SKILL.md manually (one-shot invocation) to confirm all 3 simulations initialize cleanly
- Check `memory/ark_journal.json` is written after first run
- Confirm 3 Telegram messages are sent

### Manual Verification
- Review tomorrow's Telegram messages — should see 3 reports:
  1. Main FA Report (with regime badge + score boosts displayed)
  2. Wolff Simulation Report
  3. ARK Simulation Report
- Confirm score table in HTML shows which boosts were applied
- Check git to confirm new files are tracked

---

## Open Questions

> [!NOTE]
> ARK publishes daily CSVs but the URL format can change. If scraping fails, the fallback is to manually seed `ark_journal.json` with ARKK's top holdings (available publicly from ETF.com). The agent will skip the ARK sim for that day and report the failure gracefully.

> [!IMPORTANT]
> The Earnings Calendar "BLOCK" rule (no new position the day before an earnings report) applies only to **new** buys. If you already hold the stock, the agent will follow normal stop-loss / trailing stop rules — it will NOT auto-sell before earnings.
