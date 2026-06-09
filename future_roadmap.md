# Agentic FA - Future Improvements Roadmap

This document outlines "nice-to-have" enhancements and future improvements for the Agentic FA trading system. These features were brainstormed during the Phase 2 intelligence upgrades and can be implemented after the current two-week monitoring period.

## 1. Sentiment Analysis Integration
**Description:** Incorporate a social media sentiment scraper (e.g., Twitter/X, Reddit's r/wallstreetbets) to gauge retail sentiment and momentum.
**Implementation Idea:** 
- Add a new "sentiment_score" metric to the scoring pipeline.
- Boost scores (+0.5 to +1.0) for tickers with high positive sentiment volume.
- Penalize scores (-1.0) for tickers experiencing sudden negative sentiment spikes.

## 2. Dynamic Auto-Stop-Loss & Take-Profit
**Description:** Implement programmatic sell triggers based on dynamic thresholds rather than static percentages.
**Implementation Idea:**
- Instead of a fixed -8% stop-loss or +10% take-profit, adjust these based on the asset's historical volatility (e.g., Average True Range - ATR).
- Implement trailing stop-losses to lock in gains as a position trends upward.

## 3. Direct Broker Integration (Paper Trading)
**Description:** Move beyond pure local simulation by integrating with a paper trading API (like Alpaca or an official Robinhood paper trading environment if available).
**Implementation Idea:**
- Bridge the `journal.json` decisions with actual API calls to place paper orders.
- This allows tracking realistic slippage, fill rates, and execution times compared to the current simulated fill prices.

## 4. Sector Diversification Module
**Description:** Introduce risk management controls to prevent the portfolio from becoming over-concentrated in a single sector (e.g., tech or biotech).
**Implementation Idea:**
- Add a pre-trade check that calculates current sector exposure.
- Automatically reject or scale down buy orders if adding the position would cause a single sector to exceed 20% of the total portfolio value.

## 5. Advanced Macro Regime Detection
**Description:** Expand the current VIX/SPX Moving Average regime classification to include more macro indicators.
**Implementation Idea:**
- Integrate yield curve data (e.g., 2yr vs 10yr Treasury yields).
- Track inflation data releases (CPI/PPI) and adjust the overall portfolio cash-holding requirements (e.g., hold more cash during high uncertainty).

## 6. Options Market Flow (Unusual Whales)
**Description:** Monitor the options market for unusual volume or large block trades (sweep orders) to detect institutional positioning before stock price movement.
**Implementation Idea:**
- Pull data on call/put ratios and unusual options activity.
- Use strong bullish flow as a booster in the scoring model.

## 7. The Claude Portfolio Tracking (Simulation)
**Description:** Implement a third simulated portfolio that tracks and mimics "The Claude Portfolio" (the AI-managed stock portfolio run autonomously by Claude on the Autopilot app).
**Implementation Idea:**
- Create a `claude_journal.json` to act as the ledger for this $1,000 simulated account.
- Scrape or monitor the official X account **@theaiportfolios** (or the Autopilot app's public API/disclosure endpoint) to fetch its real-time buys, sells, and holdings.
- Execute those trades in our simulation and track its performance in a separate HTML dashboard report (`claude_simulation_report.html`).
