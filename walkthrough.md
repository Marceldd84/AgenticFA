# FA Agent — Cumulative Walkthrough

## Architecture Overview

The FA Agent is an autonomous daily trading advisor running on a Robinhood Agentic account.
It fires every trading day at 10:00 AM ET via a scheduled cron, spawns parallel research
sub-agents, scores opportunities, manages a live portfolio, and runs two parallel simulations.

**Account**: Robinhood Agentic account configured in config (never touches personal account).
**Mode**: `live` (real orders enabled). Simulation accounts are always `simulated`.
**Repo**: https://github.com/Marceldd84/AgenticFA.git

---

## Phase 1 — Initial Implementation

### What Was Built
- Core SKILL.md daily workflow (Phases 0–5)
- Robinhood MCP integration via `get_portfolio`, `get_equity_positions`, `get_equity_quotes`, `place_equity_order`
- 5-factor scoring engine (catalyst strength, price momentum, sector alignment, portfolio fit, risk/reward)
- Hard stop-loss (-8%), take-profit (+10%), trailing stop (-5% from peak) rules
- Portfolio rotation logic (sell weakest, buy strongest if ≥2.0 score gap)
- Telegram reporting via `scripts/send_telegram.py`
- 7-day rolling journal memory (`memory/journal.json`)
- Permanent trade log (`memory/trades.json`)

### Peter Wolff Flagship Simulation (Phase 1 Add-on)
- Parallel $1,000 virtual portfolio copying Peter Wolff's Substack/X disclosed picks
- Memory: `memory/wolff_journal.json` (14-day rolling), `memory/wolff_trades.json`
- Wolff picks get a **+1.5 score boost** in the live scoring engine
- Generates Report 2 (separate Telegram message + HTML dashboard)
- `config/agent_config.json` → `wolff_simulation` block

---

## Phase 2 — Intelligence Upgrade (June 9, 2026)

### Commit: `9465ada` → pushed to `main`

### 1. Macro Regime Classifier (Phase 0, Step 4)
Every morning before any analysis runs, the agent:
1. Fetches today's **VIX value** (finviz.com / CBOE)
2. Checks whether **SPX is above/below its 50-day MA** (finviz.com / macrotrends.net)
3. Classifies the day as one of three regimes:

| Regime | Condition | Cash Reserve | Min Score | New Buys? |
|---|---|---|---|---|
| 🟢 risk_on | VIX < 18 + SPX above 50-day | 10% | 6.0 | Yes |
| 🟡 cautious | VIX 18–25 or SPX near MA | 15% | 6.5 | Yes |
| 🔴 risk_off | VIX > 25 or SPX below MA | 25% | 7.5 | No |

The regime **overrides** the base config for that entire day's run.
If VIX data is unavailable → defaults to `cautious` (conservative fallback).

### 2. Earnings Calendar (Sub-Agent A, Section 4)
- Fetches today's earnings releases from Yahoo Finance / EarningsWhispers
- **Reported today**: Beat+Raised → **+2.0 boost**; Beat only → **+1.0**; Miss → **-2.0 penalty**
- **Reporting tomorrow pre-market**: Stock is **BLOCKED** from new buys today

### 3. SEC Form 4 — Insider Buying (Sub-Agent B, Section 4)
- Scrapes OpenInsider for Form 4 "Purchase" filings in the last 48 hours (>$50K)
- Cluster buys (3+ insiders, same company): **+1.0 boost**
- Large single buy (>$500K): **+0.5 boost**
- Ignores: option exercises, gifts, automatic plan transactions

### 4. Congress Trades — STOCK Act (Sub-Agent B, Section 5)
- Scrapes QuiverQuant for congressional stock purchases in the last 7 days
- Purchases only (not sales, not ETFs)
- 3+ members buying same ticker: **+1.0 boost**
- 1–2 members buying: **+0.5 boost**

### 5. ARK Invest ARKK Holdings (Sub-Agent B, Section 7)
- Fetches ARKK's daily disclosed holdings CSV from ark-funds.com
- ARK's recent buys (last 3 trading days) trigger a **+0.75 boost** to the live engine
- Data used for Phase 3.6 ARK simulation

### 6. Expanded Score Modifier Table (Phase 2D)
All modifiers are additive, **capped at +4.0 total per stock**:
| Signal | Modifier |
|---|---|
| Wolff pick | +1.5 |
| ARK recent buy | +0.75 |
| Insider cluster | +1.0 |
| Insider large single | +0.5 |
| Congress cluster | +1.0 |
| Congress single | +0.5 |
| Earnings beat+raised | +2.0 |
| Earnings beat only | +1.0 |
| Earnings miss | -2.0 |
| Earnings tomorrow | BLOCK |

### 7. ARK Invest ARKK Simulation (Phase 3.6)
Mirrors Wolff simulation architecture exactly:
- $1,000 virtual starting capital
- Tracks ARKK's top 15 holdings by disclosed weight
- Daily delta-rebalancing using Robinhood live quotes
- Memory: `memory/ark_journal.json` (14-day), `memory/ark_trades.json`
- Graceful fallback: if ARK data unavailable → skip sim, log "ARK_DATA_UNAVAILABLE"
- Config: `agent_config.json` → `ark_simulation` block

### 8. Triple Reporting System (Phase 4)
Agent now sends **3 Telegram messages** per day:
1. **Main FA Report** — live portfolio + all signal modifiers applied + macro regime badge
2. **Wolff Simulation Report** — virtual portfolio + Wolff target allocation
3. **ARK Simulation Report** (NEW) — virtual ARKK portfolio + ARK disclosed holdings

HTML dashboards (dark-mode glassmorphism):
- `reports/daily_report.html` — includes Signal Intelligence table + Macro Regime banner
- `reports/wolff_simulation_report.html` — Wolff virtual portfolio
- `reports/ark_simulation_report.html` (NEW) — ARK virtual portfolio + top-15 holdings

---

## Files Modified in Phase 2

| File | Status | Notes |
|---|---|---|
| `.gemini/skills/daily_fa/SKILL.md` | Modified | Full rewrite — Phase 2 features |
| `config/agent_config.json` | Modified (local only, gitignored) | Added `macro_regime` + `ark_simulation` |
| `memory/ark_journal.json` | Created (local only, gitignored) | ARK sim state |
| `memory/ark_trades.json` | Created (local only, gitignored) | ARK trade log |
| `.gitignore` | Modified | Added `scripts/ark_last_report.txt` |

---

## Simulation Comparison Overview

| Account | Starting Capital | Source | Score Boost to Live Engine |
|---|---|---|---|
| Live Portfolio | Real cash | Agent's own decisions | — |
| Wolff Flagship Sim | $1,000 virtual | Peter Wolff Substack/X | +1.5 per matching stock |
| ARK Invest Sim | $1,000 virtual | ARKK daily CSV | +0.75 per recent buy |

After ~2 weeks of running, you'll have a live 3-way performance comparison:
your agent vs. Wolff vs. ARK vs. SPY (implied benchmark).

---

## Scheduled Run
- **Time**: 10:00 AM ET, Monday–Friday
- **Cron UTC**: `0 14 * * 1-5` (EDT) / change to `0 15 * * 1-5` during EST (Nov–Mar)
