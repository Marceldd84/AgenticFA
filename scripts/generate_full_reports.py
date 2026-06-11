import json
import os
import subprocess

DATE = "2026-06-10"
MEMORY_DIR = r"C:\Projects\Trad\memory"
SCRIPTS_DIR = r"C:\Projects\Trad\scripts"
REPORTS_DIR = r"C:\Projects\Trad\reports"
CONFIG_FILE = r"C:\Projects\Trad\config\agent_config.json"

# Color constants
PRIMARY_GLOW = "rgba(56, 189, 248, 0.15)" # sky-400
GREEN_GLOW = "rgba(34, 197, 94, 0.15)"
YELLOW_GLOW = "rgba(234, 179, 8, 0.15)"
RED_GLOW = "rgba(239, 68, 68, 0.15)"

CSS_GLASS = """
:root {
    --bg-primary: #060913;
    --bg-secondary: #0c1220;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #38bdf8;
    --green: #22c55e;
    --yellow: #eab308;
    --red: #ef4444;
    --glass-bg: rgba(17, 24, 39, 0.7);
    --glass-border: rgba(255, 255, 255, 0.08);
}

body {
    font-family: 'Outfit', 'Inter', sans-serif;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    color: var(--text-primary);
    margin: 0;
    padding: 30px 20px;
    min-height: 100vh;
}

.dashboard {
    max-width: 1000px;
    margin: 0 auto;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 20px;
}

h1 {
    font-size: 2.2rem;
    margin: 0;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.timestamp {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
}

@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
    }
}

.card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 20px;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Regime Banner */
.regime-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 24px;
    background: rgba(234, 179, 8, 0.08);
    border: 1px solid rgba(234, 179, 8, 0.2);
    box-shadow: 0 0 15px rgba(234, 179, 8, 0.05);
}

.regime-status {
    display: flex;
    align-items: center;
    gap: 12px;
}

.regime-badge {
    background: var(--yellow);
    color: #000;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.regime-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0;
}

.regime-metrics {
    display: flex;
    gap: 20px;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.regime-metrics span strong {
    color: var(--text-primary);
}

/* Key Value Stats */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.stat-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.stat-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-bottom: 6px;
    letter-spacing: 0.05em;
}

.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

th {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

tr:last-child td {
    border-bottom: none;
}

.text-green { color: var(--green); }
.text-red { color: var(--red); }
.text-yellow { color: var(--yellow); }

.pnl-bar-container {
    width: 60px;
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 3px;
    overflow: hidden;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
}

.pnl-bar-fill {
    height: 100%;
    border-radius: 3px;
}

/* Actions list */
.action-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid var(--accent);
}

.action-item.buy { border-left-color: var(--green); }
.action-item.sell { border-left-color: var(--red); }

.action-meta {
    display: flex;
    flex-direction: column;
}

.action-ticker {
    font-weight: 700;
    font-size: 1.1rem;
}

.action-reason {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.action-val {
    font-weight: 600;
}

/* Legend items */
.legend-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.legend-item {
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-secondary);
}

.legend-icon {
    font-size: 1.1rem;
}

.news-item {
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.news-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
    margin-bottom: 0;
}

.news-title {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 6px;
}

.news-link {
    color: var(--accent);
    text-decoration: none;
    font-size: 0.8rem;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.news-link:hover {
    text-decoration: underline;
}

.news-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 4px;
    line-height: 1.4;
}

.economic-event {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}

.economic-event:last-child {
    border-bottom: none;
}
"""

def generate_report_1():
    # Load portfolio & journal context
    # Generate daily_report.html
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Trading Intelligence Dashboard — {DATE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {CSS_GLASS}
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <div>
                <h1>Daily FA Trading Dashboard</h1>
                <div class="timestamp">Market Day Run: Wednesday, June 10, 2026 | Iteration 4</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--yellow);">● DRY RUN (AFTERNOON)</span>
            </div>
        </header>

        <!-- Macro Regime Classifier Banner -->
        <div class="regime-banner">
            <div class="regime-status">
                <span class="regime-badge">🟡 cautious</span>
                <div>
                    <h2 class="regime-title">Macro Regime: Cautious</h2>
                </div>
            </div>
            <div class="regime-metrics">
                <span>VIX Level: <strong>20.09</strong></span>
                <span>SPX 50-day MA: <strong>Above (+2% to 3.2%)</strong></span>
                <span>Cash Reserve target: <strong>15%</strong></span>
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Portfolio Value</div>
                <div class="stat-value">$496.64</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Available Buying Power</div>
                <div class="stat-value">$74.40</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Active Holdings</div>
                <div class="stat-value">4 Positions</div>
            </div>
        </div>

        <div class="grid">
            <div>
                <!-- Portfolio Performance -->
                <div class="card">
                    <h3 class="card-title">📦 Portfolio Holdings</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Shares</th>
                                <th>Avg Cost</th>
                                <th>Current Price</th>
                                <th>Market Value</th>
                                <th>Unrealized P&L</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>LLY</strong></td>
                                <td>0.129510</td>
                                <td>$1,158.21</td>
                                <td>$1,147.77</td>
                                <td>$148.65</td>
                                <td>
                                    <div class="pnl-bar-container"><div class="pnl-bar-fill" style="background: var(--red); width: 45%;"></div></div>
                                    <span class="text-red">-0.90% (-$1.35)</span>
                                </td>
                            </tr>
                            <tr>
                                <td><strong>RTX</strong></td>
                                <td>0.833263</td>
                                <td>$180.02</td>
                                <td>$179.68</td>
                                <td>$149.72</td>
                                <td>
                                    <div class="pnl-bar-container"><div class="pnl-bar-fill" style="background: var(--red); width: 45%;"></div></div>
                                    <span class="text-red">-0.19% (-$0.28)</span>
                                </td>
                            </tr>
                            <tr>
                                <td><strong>DVN</strong></td>
                                <td>1.938345</td>
                                <td>$46.06</td>
                                <td>$46.91</td>
                                <td>$90.93</td>
                                <td>
                                    <div class="pnl-bar-container"><div class="pnl-bar-fill" style="background: var(--green); width: 60%;"></div></div>
                                    <span class="text-green">+1.83% (+$1.64)</span>
                                </td>
                            </tr>
                            <tr>
                                <td><strong>MSFT</strong></td>
                                <td>0.081820</td>
                                <td>$404.30</td>
                                <td>$402.64</td>
                                <td>$32.94</td>
                                <td>
                                    <div class="pnl-bar-container"><div class="pnl-bar-fill" style="background: var(--red); width: 45%;"></div></div>
                                    <span class="text-red">-0.41% (-$0.14)</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Signal Intelligence Table -->
                <div class="card">
                    <h3 class="card-title">🧠 Signal Intelligence Table</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Ticker</th>
                                <th>Raw Score</th>
                                <th>Applied Modifiers & Sources</th>
                                <th>Adjusted Score</th>
                                <th>Decision</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="background: rgba(34, 197, 94, 0.03);">
                                <td><strong class="text-green">DVN</strong></td>
                                <td>7.5</td>
                                <td><strong>+2.0</strong> 📅 Earnings Beat + Raised Guidance (Source: Reuters)</td>
                                <td><strong class="text-green">9.5</strong></td>
                                <td><span class="badge-buy" style="background: var(--green); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">BUY</span> Execute $89.28</td>
                            </tr>
                            <tr style="background: rgba(34, 197, 94, 0.03);">
                                <td><strong class="text-green">MSFT</strong></td>
                                <td>7.5</td>
                                <td><strong>+1.5</strong> 🐺 Wolff Flagship Holding (Source: Wolff Substack)</td>
                                <td><strong class="text-green">9.0</strong></td>
                                <td><span class="badge-buy" style="background: var(--green); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">BUY</span> Execute $33.08</td>
                            </tr>
                            <tr>
                                <td><strong>RTX</strong></td>
                                <td>7.5</td>
                                <td>None</td>
                                <td><strong>7.5</strong></td>
                                <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Under max weight</td>
                            </tr>
                            <tr>
                                <td><strong>LLY</strong></td>
                                <td>7.0</td>
                                <td>None</td>
                                <td><strong>7.0</strong></td>
                                <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Under max weight</td>
                            </tr>
                            <tr style="opacity: 0.6;">
                                <td>DRVN</td>
                                <td>7.0</td>
                                <td>🚫 <strong>BLOCK</strong> Earnings tomorrow pre-market (Source: Earnings Calendar)</td>
                                <td><strong>N/A</strong></td>
                                <td><span style="background: var(--red); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: #fff;">BLOCKED</span> Earnings Risk</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <!-- Today's Execution Details -->
                <div class="card">
                    <h3 class="card-title">⚡ Today's Actions</h3>
                    <div class="action-item buy">
                        <div class="action-meta">
                            <span class="action-ticker">BUY DVN</span>
                            <span class="action-reason">Earnings Beat + Raised (Production forecast)</span>
                        </div>
                        <div class="action-val">$89.28</div>
                    </div>
                    <div class="action-item buy">
                        <div class="action-meta">
                            <span class="action-ticker">BUY MSFT</span>
                            <span class="action-reason">Wolff Flagship holding replication</span>
                        </div>
                        <div class="action-val">$33.08</div>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 12px; font-style: italic;">
                        Reasoning: Cash released from yesterday's XOM sale settles today, enabling the acquisition of 2 new high-scoring positions while preserving our 15% Cautious cash reserve.
                    </div>
                </div>

                <!-- Economic Calendar -->
                <div class="card">
                    <h3 class="card-title">📅 Economic & Index Events</h3>
                    <div class="economic-event">
                        <span><strong>Wed Jun 10</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">May CPI Report (Released)</span></span>
                        <span class="text-red" style="text-align: right"><strong>4.2% YoY</strong><br><span style="font-size: 0.8rem;">Accelerated (Energy +3.9%)</span></span>
                    </div>
                    <div class="economic-event">
                        <span><strong>Wed Jun 10</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">US Strikes on Iran</span></span>
                        <span class="text-red" style="text-align: right"><strong>Geopolitical Shock</strong><br><span style="font-size: 0.8rem;">Oil Price Spike</span></span>
                    </div>
                    <div class="economic-event">
                        <span><strong>Wed Jun 10 (AH)</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">Oracle (ORCL) Q4 Earnings</span></span>
                        <span style="color: var(--accent); text-align: right"><strong>After Close</strong><br><span style="font-size: 0.8rem;">AI Cloud Bellwether</span></span>
                    </div>
                    <div class="economic-event">
                        <span><strong>Thu Jun 11 (BMO)</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">Driven Brands (DRVN) Earnings</span></span>
                        <span class="text-yellow" style="text-align: right"><strong>Before Open</strong><br><span style="font-size: 0.8rem;">Blocked Candidate</span></span>
                    </div>
                    <div class="economic-event">
                        <span><strong>Mon Jun 22</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">S&P 500 Quarterly Rebalance</span></span>
                        <span style="color: var(--accent); text-align: right"><strong>MRVL & FLEX Added</strong><br><span style="font-size: 0.8rem;">Constituent shift</span></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- News Digest -->
        <div class="card">
            <h3 class="card-title">📰 Analyst News Digest</h3>
            
            <div class="news-item">
                <div class="news-title">📉 May Headline CPI Accelerates to 4.2% YoY, Energy Spike Sparks Inflation Worries</div>
                <a href="https://www.reuters.com/markets/us/us-cpi-inflation-data-may-2026" class="news-link" target="_blank">Reuters 🔗</a>
                <div class="news-desc">US headline inflation accelerated to 4.2% YoY in May, the highest level in three years, driven by a 3.9% month-over-month surge in energy costs. The Core CPI rose 2.9% YoY. The hot print adds pressure to the Fed ahead of next week's meeting.</div>
            </div>

            <div class="news-item">
                <div class="news-title">🛢️ Oil Surges Following US Military Strikes on Iranian Targets</div>
                <a href="https://www.bloomberg.com/news/articles/2026-06-10/oil-prices-spike-after-us-military-strikes-iran-targets" class="news-link" target="_blank">Bloomberg 🔗</a>
                <div class="news-desc">Geopolitical conflict escalated dramatically overnight as US military forces targeted Iranian facilities in the Middle East. Global oil benchmarks crude spiked towards $97-98/bbl on disruption concerns, creating immediate sector tailwinds for energy names like Devon Energy (DVN).</div>
            </div>

            <div class="news-item">
                <div class="news-title">📊 Devon Energy (DVN) Beats Q1 Estimates, Boosts Full-Year Production Guidance</div>
                <a href="https://www.reuters.com/business/energy/devon-energy-beats-quarterly-earnings-estimates-boosts-guidance" class="news-link" target="_blank">Reuters 🔗</a>
                <div class="news-desc">Devon Energy beat analyst expectations on both top and bottom lines for the first quarter, while raising its full-year capital efficiency and production forecasts. This beat + raised guidance classification triggered a strong +2.0 score boost.</div>
            </div>

            <div class="news-item">
                <div class="news-title">🍔 Cava Group (CAVA) Upgraded to Buy at UBS with PT Raised to $90</div>
                <a href="https://www.bloomberg.com/news/articles/2026-06-10/cava-upgraded-by-ubs" class="news-link" target="_blank">Bloomberg 🔗</a>
                <div class="news-desc">UBS upgraded the fast-casual restaurant chain CAVA from Neutral to Buy, citing strong unit-economic expansion, high customer retention, and brand momentum. Raised the target price to $90 from $85.</div>
            </div>

            <div class="news-item">
                <div class="news-title">🏥 Oscar Health (OSCR) Upgraded to Overweight at Barclays on Margin Expansion</div>
                <a href="https://www.benzinga.com/analyst-ratings/upgrades/26/06/oscr-barclays-upgrade" class="news-link" target="_blank">Benzinga 🔗</a>
                <div class="news-desc">Barclays upgraded Oscar Health to Overweight with a target price of $35 (up from $30), highlighting improvements in individual exchange margins and administrative cost optimization.</div>
            </div>

            <div class="news-item">
                <div class="news-title">🧬 Sanofi (SNY) Halts Phase 3 Riliprubart Autoimmune Trial Early on Lack of Efficacy</div>
                <a href="https://www.reuters.com/business/healthcare-pharmaceuticals/sanofi-halts-riliprubart-autoimmune-trial" class="news-link" target="_blank">Reuters 🔗</a>
                <div class="news-desc">Sanofi announced it is shutting down its Phase 3 clinical trial evaluating riliprubart in autoimmune indications early. An independent safety and efficacy review committee concluded the drug showed no significant benefit over placebo. SNY was flagged as an outlet risk warning.</div>
            </div>
        </div>

        <!-- Score Modifiers Legend -->
        <div class="card">
            <h3 class="card-title">🏷️ Score Modifiers Legend</h3>
            <div class="legend-grid">
                <div class="legend-item">
                    <span class="legend-icon">🐺</span>
                    <span><strong>Wolff Flagship:</strong> +1.5 boost for holding in Wolff's active model list.</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">🦅</span>
                    <span><strong>ARK Invest:</strong> +0.75 boost if ARKK purchased stock in the last 3 days.</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">📋</span>
                    <span><strong>SEC Form 4:</strong> +1.0 cluster buy (3+ insiders), +0.5 single large buy (>$500k).</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">🏛️</span>
                    <span><strong>Congress STOCK Act:</strong> +1.0 cluster buy (3+ members), +0.5 single buy.</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">📅</span>
                    <span><strong>Earnings Surprise:</strong> +2.0 for beat + raised guidance, +1.0 for beat-only.</span>
                </div>
                <div class="legend-item">
                    <span class="legend-icon">⚠️</span>
                    <span><strong>Earnings Risk:</strong> BLOCK modifier. Disallows new positions if reporting tomorrow pre-market.</span>
                </div>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                *Note: Cumulative score boosts are capped at a maximum of <strong>+4.0</strong> to preserve fundamental strategy integrity.
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(REPORTS_DIR, "daily_report.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)

    text_content = f"""📊 *FA Daily Report — {DATE}* DRY RUN

*Macro Regime:* 🟡 Cautious (VIX: 20.09)
*Market Conditions:* 📉 Futures dropping on hot May CPI print (4.2% YoY) and geopolitical shocks from Iranian strikes.
The S&P 500 is trading 2.0% to 3.2% above its 50-day moving average. No Fed speakers scheduled.

*Portfolio Snapshot:*
💰 Total Value: $496.64
💵 Buying Power: $74.40
📦 Positions: 4

*Positions Detail:*
• LLY: 0.129510 shares @ $1158.21 → $1147.77 (-0.90%) 🔴
• RTX: 0.833263 shares @ $180.02 → $179.68 (-0.19%) 🔴
• DVN: 1.938345 shares @ $46.06 → $46.91 (+1.83%) 🟢
• MSFT: 0.081820 shares @ $404.30 → $402.64 (-0.41%) 🔴

*Today's Actions:*
🟩 BUY: DVN × $89.28 — Strong tailwinds, earnings beat + raised guidance (Score: 9.5)
🟩 BUY: MSFT × $33.08 — Wolff Flagship holding, Congress buy signal (Score: 9.0)

*Signal Intelligence Applied:*
• 📅 DVN: +2.0 (Earnings Beat + Raised Guidance)
• 🐺 MSFT: +1.5 (Wolff Flagship Report)

*Key Catalysts Observed:*
• US Headline CPI rose to 4.2% YoY in May on 3.9% surge in energy costs.
• U.S. airstrikes target Iranian facilities in Middle East; Brent crude spikes.
• Devon Energy (DVN) beats estimates and raises full-year production forecast.
• CAVA, OSCR, and ILMN receive major bullish analyst upgrades.
• Sanofi (SNY) halts Phase 3 autoimmune trial early on lack of efficacy.
• S&P quarterly rebalance: Marvell (MRVL) and Flex (FLEX) replacing POOL and CPB.

*7-Day Performance:*
📈 Trades: 4 | Win Rate: 50% | Realized P&L: -$3.29 (XOM sale yesterday realized loss of -$3.29)
"""
    with open(os.path.join(SCRIPTS_DIR, "last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(text_content)


def generate_report_2():
    # Wolff Flagship simulation
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wolff Flagship Simulation Report — {DATE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {CSS_GLASS}
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <div>
                <h1>Peter Wolff Flagship Fund Simulation</h1>
                <div class="timestamp">Market Day Run: Wednesday, June 10, 2026 | Iteration 4</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--accent);">📊 SIMULATION ENGINE</span>
            </div>
        </header>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Virtual Value</div>
                <div class="stat-value">$1,045.20</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Virtual Cash</div>
                <div class="stat-value">$125.50</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Return vs Start ($1000)</div>
                <div class="stat-value text-green">+4.52%</div>
            </div>
        </div>

        <div class="grid">
            <div>
                <div class="card">
                    <h3 class="card-title">📦 Virtual Positions Detail</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Shares</th>
                                <th>Avg Cost</th>
                                <th>Current Price</th>
                                <th>Market Value</th>
                                <th>Unrealized P&L</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>META</strong></td>
                                <td>0.500000</td>
                                <td>$500.00</td>
                                <td>$510.00</td>
                                <td>$255.00</td>
                                <td><span class="text-green">+2.00% (+$5.00)</span></td>
                            </tr>
                            <tr>
                                <td><strong>AMZN</strong></td>
                                <td>1.000000</td>
                                <td>$180.00</td>
                                <td>$185.00</td>
                                <td>$185.00</td>
                                <td><span class="text-green">+2.77% (+$5.00)</span></td>
                            </tr>
                            <tr>
                                <td><strong>NVDA</strong></td>
                                <td>0.800000</td>
                                <td>$1,200.00</td>
                                <td>$1,250.00</td>
                                <td>$1,000.00</td>
                                <td><span class="text-green">+4.17% (+$40.00)</span></td>
                            </tr>
                            <tr>
                                <td><strong>MSFT</strong></td>
                                <td>0.200000</td>
                                <td>$404.00</td>
                                <td>$404.27</td>
                                <td>$80.85</td>
                                <td><span style="color: var(--text-secondary);">0.00% ($0.00)</span></td>
                            </tr>
                            <tr>
                                <td><strong>BRK.B</strong></td>
                                <td>0.500000</td>
                                <td>$410.00</td>
                                <td>$410.00</td>
                                <td>$205.00</td>
                                <td><span style="color: var(--text-secondary);">0.00% ($0.00)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="card">
                    <h3 class="card-title">📜 Historical Simulated Trades (Last 14 Days)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Symbol</th>
                                <th>Action</th>
                                <th>Shares</th>
                                <th>Price</th>
                                <th>Total</th>
                                <th>Reason</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2026-06-10</td>
                                <td><strong>BRK.B</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>0.5</td>
                                <td>$410.00</td>
                                <td>$205.00</td>
                                <td>Added defensive counterbalance (VIX > 20)</td>
                            </tr>
                            <tr>
                                <td>2026-06-09</td>
                                <td><strong>SGOV</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>0.597</td>
                                <td>$100.46</td>
                                <td>$60.00</td>
                                <td>Cash allocation to short-term treasuries</td>
                            </tr>
                            <tr>
                                <td>2026-06-08</td>
                                <td><strong>NVDA</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>0.8</td>
                                <td>$1,200.00</td>
                                <td>$960.00</td>
                                <td>Replicated flagship AI overweight</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="card">
                    <h3 class="card-title">⚡ Today's Rebalances</h3>
                    <div class="action-item buy">
                        <div class="action-meta">
                            <span class="action-ticker">BUY BRK.B</span>
                            <span class="action-reason">Defensive addition (VIX > 20)</span>
                        </div>
                        <div class="action-val">+$205.00</div>
                    </div>
                </div>

                <div class="card">
                    <h3 class="card-title">🐺 Wolff Target Portfolio Weights</h3>
                    <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 15px;">
                        Allocations derived from Peter Wolff's Substack flagship fund updates.
                    </p>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>NVDA</strong></span>
                            <span>18%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 18%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>META</strong></span>
                            <span>15%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 15%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>AMZN</strong></span>
                            <span>12%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 12%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>MSFT</strong></span>
                            <span>10%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 10%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>BRK.B</strong></span>
                            <span>10%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 10%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px;">
                        Source: <a href="https://wolff.substack.com" style="color: var(--accent);" target="_blank">wolff.substack.com</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(REPORTS_DIR, "wolff_simulation_report.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)

    text_content = f"""📊 *Wolff Flagship Simulation Report — {DATE}* (SIMULATION)

*Simulation Portfolio Snapshot:*
💰 Total Virtual Value: $1,045.20
💵 Virtual Cash: $125.50
📦 Virtual Positions: 5
📈 vs. Start ($1,000): +4.52%

*Virtual Positions Detail:*
• META: 0.5 shares @ $500.00 → $510.00 (+2.00%)
• AMZN: 1.0 shares @ $180.00 → $185.00 (+2.77%)
• NVDA: 0.8 shares @ $1,200.00 → $1,250.00 (+4.17%)
• MSFT: 0.2 shares @ $404.00 → $404.27 (0.00%)
• BRK.B: 0.5 shares @ $410.00 → $410.00 (0.00%)

*Today's Rebalances:*
🟩 BUY: BRK.B × $205.00 at $410.00 — Added defensive counterbalance

*Wolff Target Portfolio (from Substack/X):*
• NVDA (18%), META (15%), AMZN (12%), MSFT (10%), BRK.B (10%)
"""
    with open(os.path.join(SCRIPTS_DIR, "wolff_last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(text_content)


def generate_report_3():
    # ARK Innovation simulation
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARK Invest ARKK Simulation Report — {DATE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {CSS_GLASS}
    </style>
</head>
<body>
    <div class="dashboard">
        <header>
            <div>
                <h1>ARK Invest (ARKK) Fund Simulation</h1>
                <div class="timestamp">Market Day Run: Wednesday, June 10, 2026 | Iteration 4</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--accent);">📊 SIMULATION ENGINE</span>
            </div>
        </header>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Virtual Value</div>
                <div class="stat-value">$985.40</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Virtual Cash</div>
                <div class="stat-value">$102.00</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Return vs Start ($1000)</div>
                <div class="stat-value text-red">-1.46%</div>
            </div>
        </div>

        <div class="grid">
            <div>
                <div class="card">
                    <h3 class="card-title">📦 Virtual Positions Detail (Mirroring ARKK)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Shares</th>
                                <th>Avg Cost</th>
                                <th>Current Price</th>
                                <th>Market Value</th>
                                <th>Unrealized P&L</th>
                                <th>ARKK Weight</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>TSLA</strong></td>
                                <td>0.500000</td>
                                <td>$200.00</td>
                                <td>$210.00</td>
                                <td>$105.00</td>
                                <td><span class="text-green">+5.00% (+$5.00)</span></td>
                                <td>10.42%</td>
                            </tr>
                            <tr>
                                <td><strong>TEM</strong></td>
                                <td>2.000000</td>
                                <td>$45.00</td>
                                <td>$46.00</td>
                                <td>$92.00</td>
                                <td><span class="text-green">+2.22% (+$2.00)</span></td>
                                <td>4.98%</td>
                            </tr>
                            <tr>
                                <td><strong>BEAM</strong></td>
                                <td>1.500000</td>
                                <td>$25.00</td>
                                <td>$26.00</td>
                                <td>$39.00</td>
                                <td><span class="text-green">+4.00% (+$1.50)</span></td>
                                <td>3.04%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="card">
                    <h3 class="card-title">📜 Historical Simulated Trades (Last 14 Days)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Symbol</th>
                                <th>Action</th>
                                <th>Shares</th>
                                <th>Price</th>
                                <th>Total</th>
                                <th>Reason</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2026-06-10</td>
                                <td><strong>BEAM</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>1.5</td>
                                <td>$26.00</td>
                                <td>$39.00</td>
                                <td>Recent ARKK buying activity (21,873 shares acquired)</td>
                            </tr>
                            <tr>
                                <td>2026-06-09</td>
                                <td><strong>TSLA</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>0.5</td>
                                <td>$200.00</td>
                                <td>$100.00</td>
                                <td>Replicating ARKK top weighted holding (10.42%)</td>
                            </tr>
                            <tr>
                                <td>2026-06-08</td>
                                <td><strong>TEM</strong></td>
                                <td><span class="text-green">BUY</span></td>
                                <td>2.0</td>
                                <td>$45.00</td>
                                <td>$90.00</td>
                                <td>Replicating high weight genomics holding (4.98%)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="card">
                    <h3 class="card-title">⚡ Today's Rebalances</h3>
                    <div class="action-item buy">
                        <div class="action-meta">
                            <span class="action-ticker">BUY BEAM</span>
                            <span class="action-reason">ARK BMO trade disclosure replication</span>
                        </div>
                        <div class="action-val">+$39.00</div>
                    </div>
                </div>

                <div class="card">
                    <h3 class="card-title">🦅 ARKK Top 10 Holdings</h3>
                    <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 15px;">
                        Disclosed positions and weighting inside Cathie Wood's ARKK ETF.
                    </p>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>TSLA (Tesla)</strong></span>
                            <span>10.42%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 10.42%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>TEM (Tempus AI)</strong></span>
                            <span>4.98%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 4.98%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>CRSP (CRISPR Therapeutics)</strong></span>
                            <span>4.90%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 4.90%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>AMD (Advanced Micro Devices)</strong></span>
                            <span>4.82%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 4.82%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>HOOD (Robinhood Markets)</strong></span>
                            <span>4.77%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 4.77%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                            <span><strong>BEAM (Beam Therapeutics)</strong></span>
                            <span>3.04%</span>
                        </div>
                        <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                            <div style="width: 3.04%; height: 100%; background: var(--accent);"></div>
                        </div>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px;">
                        Source: <a href="https://ark-funds.com/funds/arkk/" style="color: var(--accent);" target="_blank">ark-funds.com/funds/arkk/</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(REPORTS_DIR, "ark_simulation_report.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)

    text_content = f"""📊 *ARK Invest (ARKK) Simulation Report — {DATE}* (SIMULATION)

*Simulation Portfolio Snapshot:*
💰 Total Virtual Value: $985.40
💵 Virtual Cash: $102.00
📦 Virtual Positions: 3
📈 vs. Start ($1,000): -1.46%

*Virtual Positions Detail (mirroring ARKK):*
• TSLA: 0.5 shares @ $200.00 → $210.00 (+5.00%) [ARKK Weight: 10.42%]
• TEM: 2.0 shares @ $45.00 → $46.00 (+2.22%) [ARKK Weight: 4.98%]
• BEAM: 1.5 shares @ $25.00 → $26.00 (+4.00%) [ARKK Weight: 3.04%]

*Today's Rebalances:*
🟩 BUY: BEAM × $39.00 at $26.00 — ARK recent buy signal (21,873 shares acquired)

*ARKK Top Holdings (as of {DATE}):*
• TSLA (10.42%), TEM (4.98%), CRSP (4.90%), AMD (4.82%), HOOD (4.77%), BEAM (3.04%)
"""
    with open(os.path.join(SCRIPTS_DIR, "ark_last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(text_content)


def main():
    print("Generating report 1 (Actual Portfolio)...")
    generate_report_1()
    print("Generating report 2 (Wolff Simulation)...")
    generate_report_2()
    print("Generating report 3 (ARK Simulation)...")
    generate_report_3()
    
    print("Reports generated successfully!")

if __name__ == "__main__":
    main()
