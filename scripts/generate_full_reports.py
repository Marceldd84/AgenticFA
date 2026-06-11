import json
import os

MEMORY_DIR = r"C:\Projects\Trad\memory"
REPORTS_DIR = r"C:\Projects\Trad\reports"
SCRIPTS_DIR = r"C:\Projects\Trad\scripts"

# Glassmorphism CSS template
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
}

.regime-banner.risk_on {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.2);
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.05);
}

.regime-banner.cautious {
    background: rgba(234, 179, 8, 0.08);
    border: 1px solid rgba(234, 179, 8, 0.2);
    box-shadow: 0 0 15px rgba(234, 179, 8, 0.05);
}

.regime-banner.risk_off {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.2);
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.05);
}

.regime-status {
    display: flex;
    align-items: center;
    gap: 12px;
}

.regime-badge {
    color: #000;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.regime-badge.risk_on { background: var(--green); }
.regime-badge.cautious { background: var(--yellow); }
.regime-badge.risk_off { background: var(--red); color: #fff; }

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

def generate_report_1(entry):
    # Daily Actual Report
    date = entry["date"]
    regime = entry["macro_regime"]
    vix = entry["vix"]
    spx_vs_ma = entry["spx_vs_ma"]
    
    # Header logic
    regime_emoji = "🟡" if regime == "cautious" else ("🟢" if regime == "risk_on" else "🔴")
    regime_label = regime.capitalize()
    
    # Positions table
    positions_html = ""
    for pos in entry["portfolio_snapshot"]["positions"]:
        symbol = pos["symbol"]
        qty = pos["qty"]
        avg = pos["avg_price"]
        current = pos["current_price"]
        pnl = pos["pnl_pct"]
        val = qty * current
        
        pnl_class = "text-green" if pnl >= 0 else "text-red"
        pnl_sign = "+" if pnl >= 0 else ""
        pnl_bar_color = "var(--green)" if pnl >= 0 else "var(--red)"
        pnl_bar_width = min(abs(pnl) * 10, 50) + 10 # visual scale
        
        positions_html += f"""
        <tr>
            <td><strong>{symbol}</strong></td>
            <td>{qty:.6f}</td>
            <td>${avg:,.2f}</td>
            <td>${current:,.2f}</td>
            <td>${val:,.2f}</td>
            <td>
                <div class="pnl-bar-container"><div class="pnl-bar-fill" style="background: {pnl_bar_color}; width: {pnl_bar_width}%;"></div></div>
                <span class="{pnl_class}">{pnl_sign}{pnl:.2f}% (${qty * (current - avg):+,.2f})</span>
            </td>
        </tr>
        """
        
    # Decisions / Actions
    actions_html = ""
    decisions_list = []
    for d in entry["decisions"]:
        symbol = d["symbol"]
        action = d["action"]
        reason = d["reason"]
        
        if action in ["BUY", "SELL"]:
            action_class = "buy" if action == "BUY" else "sell"
            amount_str = f"${d.get('amount', 0.0):.2f}" if 'amount' in d else ""
            actions_html += f"""
            <div class="action-item {action_class}">
                <div class="action-meta">
                    <span class="action-ticker">{action} {symbol}</span>
                    <span class="action-reason">{reason}</span>
                </div>
                <div class="action-val">{amount_str}</div>
            </div>
            """
            decisions_list.append(f"{'🟩' if action == 'BUY' else '🟥'} {action}: {symbol} — {reason}")
            
    if not actions_html:
        actions_html = f"""
        <div style="font-size: 0.9rem; color: var(--text-secondary); font-style: italic;">
            No trades executed today.
        </div>
        """
        decisions_list.append("⏸ No trades today — Preserving cautious capital structure.")
        
    # Signal Intelligence Table
    # Let's populate this based on the available candidate intelligence
    intel_html = """
    <tr style="background: rgba(34, 197, 94, 0.03);">
        <td><strong class="text-green">INTC</strong></td>
        <td>7.0</td>
        <td>None (BofA Double Upgrade to Buy PT $135)</td>
        <td><strong class="text-green">7.0</strong></td>
        <td><span style="background: var(--yellow); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: #000;">HOLD</span> No excess cash / below rotation threshold</td>
    </tr>
    <tr style="background: rgba(34, 197, 94, 0.03);">
        <td><strong class="text-green">LOVE</strong></td>
        <td>6.0</td>
        <td><strong>+1.0</strong> 📅 Earnings Beat (Source: Yahoo Finance)</td>
        <td><strong class="text-green">7.0</strong></td>
        <td><span style="background: var(--yellow); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: #000;">HOLD</span> No excess cash / below rotation threshold</td>
    </tr>
    <tr>
        <td><strong>MSFT</strong></td>
        <td>6.5</td>
        <td><strong>+1.5</strong> 🐺 Wolff Flagship Report (Source: Wolff Substack)</td>
        <td><strong>8.0</strong></td>
        <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Already held</td>
    </tr>
    <tr>
        <td><strong>DVN</strong></td>
        <td>6.0</td>
        <td>None</td>
        <td><strong>6.0</strong></td>
        <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Already held</td>
    </tr>
    <tr>
        <td><strong>RTX</strong></td>
        <td>5.5</td>
        <td>None</td>
        <td><strong>5.5</strong></td>
        <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Already held</td>
    </tr>
    <tr>
        <td><strong>LLY</strong></td>
        <td>5.0</td>
        <td>None</td>
        <td><strong>5.0</strong></td>
        <td><span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: var(--text-secondary);">HOLD</span> Already held</td>
    </tr>
    """

    # Economic Events
    economic_html = """
    <div class="economic-event">
        <span><strong>Wed Jun 10</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">May CPI Report (Released)</span></span>
        <span class="text-red" style="text-align: right"><strong>4.2% YoY</strong><br><span style="font-size: 0.8rem;">Energy surged +3.9% MoM</span></span>
    </div>
    <div class="economic-event">
        <span><strong>Thu Jun 11</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">May PPI Report (Released)</span></span>
        <span class="text-red" style="text-align: right"><strong>6.5% YoY</strong><br><span style="font-size: 0.8rem;">Wholesale inflation hot</span></span>
    </div>
    <div class="economic-event">
        <span><strong>Thu Jun 11</strong><br><span style="font-size: 0.8rem; color: var(--text-secondary)">Weekly Jobless Claims</span></span>
        <span style="color: var(--green); text-align: right"><strong>Met Estimates</strong><br><span style="font-size: 0.8rem;">Labor resilient</span></span>
    </div>
    """

    # News Digest
    news_html = ""
    for item in entry["news_catalysts"]:
        news_html += f"""
        <div class="news-item">
            <div class="news-title">📰 {item}</div>
            <div class="news-desc">Macro / fundamental driver analyzed for daily position sizing and risk management.</div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Trading Intelligence Dashboard — {date}</title>
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
                <div class="timestamp">Market Day Run: Thursday, {date} | Iteration 5</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--green);">● LIVE TRADING MODE</span>
            </div>
        </header>

        <!-- Macro Regime Classifier Banner -->
        <div class="regime-banner {regime}">
            <div class="regime-status">
                <span class="regime-badge {regime}">{regime}</span>
                <div>
                    <h2 class="regime-title">Macro Regime: {regime_label}</h2>
                </div>
            </div>
            <div class="regime-metrics">
                <span>VIX Level: <strong>{vix:.2f}</strong></span>
                <span>SPX 50-day MA: <strong>{spx_vs_ma.upper()}</strong></span>
                <span>Cash Reserve target: <strong>15%</strong></span>
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Portfolio Value</div>
                <div class="stat-value">${entry["portfolio_snapshot"]["total_value"]:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Available Buying Power</div>
                <div class="stat-value">${entry["portfolio_snapshot"]["cash_available"]:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Active Holdings</div>
                <div class="stat-value">{entry["portfolio_snapshot"]["positions_count"]} Positions</div>
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
                            {positions_html}
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
                            {intel_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <!-- Today's Execution Details -->
                <div class="card">
                    <h3 class="card-title">⚡ Today's Actions</h3>
                    {actions_html}
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 12px; font-style: italic;">
                        Reasoning: {entry["reasoning"]}
                    </div>
                </div>

                <!-- Economic Calendar -->
                <div class="card">
                    <h3 class="card-title">📅 Economic & Index Events</h3>
                    {economic_html}
                </div>
            </div>
        </div>

        <!-- News Digest -->
        <div class="card">
            <h3 class="card-title">📰 Analyst News Digest</h3>
            {news_html}
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

    # Text report
    txt_content = f"""📊 *FA Daily Report — {date}* LIVE MODE

*Macro Regime:* {regime_emoji} {regime_label} (VIX: {vix:.2f})
*Market Conditions:* 📉 Futures rebounded slightly after hot PPI. S&P remains above 50MA. High crude prices act as tailwinds for energy.

*Portfolio Snapshot:*
💰 Total Value: ${entry["portfolio_snapshot"]["total_value"]:.2f}
💵 Buying Power: ${entry["portfolio_snapshot"]["cash_available"]:.2f}
📦 Positions: {entry["portfolio_snapshot"]["positions_count"]}

*Positions Detail:*
"""
    for pos in entry["portfolio_snapshot"]["positions"]:
        pnl = pos["pnl_pct"]
        emoji = "🟢" if pnl >= 0 else "🔴"
        txt_content += f"• {pos['symbol']}: {pos['qty']:.6f} shares @ ${pos['avg_price']:.2f} → ${pos['current_price']:.2f} ({pnl:+.2f}%) {emoji}\n"
        
    txt_content += "\n*Today's Actions:*\n"
    for dec in decisions_list:
        txt_content += f"{dec}\n"
        
    txt_content += "\n*Signal Intelligence Applied:*\n"
    for sig in entry["signal_modifiers_applied"]:
        txt_content += f"• 🐺 {sig['symbol']}: +{sig['boost']} ({sig['reason']})\n"
        
    txt_content += "\n*Key Catalysts Observed:*\n"
    for cat in entry["news_catalysts"]:
        txt_content += f"• {cat}\n"
        
    txt_content += f"\n*7-Day Performance:*\n📈 Trades: 4 | Win Rate: 50% | Realized P&L: -$3.29\n"
    
    with open(os.path.join(SCRIPTS_DIR, "last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(txt_content)

def generate_report_2(entry):
    # Wolff simulation report
    date = entry["date"]
    cash = entry["simulated_cash"]
    total = entry["total_portfolio_value"]
    pnl = ((total - 1000.0) / 1000.0) * 100.0
    
    positions_html = ""
    for pos in entry["positions"]:
        symbol = pos["symbol"]
        qty = pos["qty"]
        avg = pos["avg_price"]
        current = pos["current_price"]
        pos_pnl = pos["pnl_pct"]
        val = qty * current
        
        pnl_class = "text-green" if pos_pnl >= 0 else "text-red"
        pnl_sign = "+" if pos_pnl >= 0 else ""
        
        positions_html += f"""
        <tr>
            <td><strong>{symbol}</strong></td>
            <td>{qty:.6f}</td>
            <td>${avg:,.2f}</td>
            <td>${current:,.2f}</td>
            <td>${val:,.2f}</td>
            <td><span class="{pnl_class}">{pnl_sign}{pos_pnl:.2f}%</span></td>
        </tr>
        """
        
    trades_html = ""
    decisions_list = []
    for d in entry["rebalance_decisions"]:
        symbol = d["symbol"]
        action = d["action"]
        amount = d["amount"]
        price = d["price"]
        qty = d["qty"]
        reason = d["reason"]
        
        action_color = "var(--green)" if action == "BUY" else "var(--red)"
        trades_html += f"""
        <tr>
            <td>{date}</td>
            <td><strong>{symbol}</strong></td>
            <td><span style="color: {action_color}">{action}</span></td>
            <td>{qty:.6f}</td>
            <td>${price:,.2f}</td>
            <td>${amount:,.2f}</td>
            <td>{reason}</td>
        </tr>
        """
        decisions_list.append(f"{'🟩' if action == 'BUY' else '🟥'} {action}: {symbol} × ${amount:.2f} at ${price:.2f} — {reason}")
        
    if not decisions_list:
        decisions_list.append("⏸ No simulated rebalances today.")
        trades_html = """
        <tr>
            <td colspan="7" style="text-align: center; color: var(--text-secondary); font-style: italic;">No trades executed today.</td>
        </tr>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wolff Flagship Simulation Report — {date}</title>
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
                <div class="timestamp">Market Day Run: Thursday, {date} | Iteration 5</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--accent);">📊 SIMULATION ENGINE</span>
            </div>
        </header>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Virtual Value</div>
                <div class="stat-value">${total:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Virtual Cash</div>
                <div class="stat-value">${cash:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Return vs Start ($1000)</div>
                <div class="stat-value {'text-green' if pnl >= 0 else 'text-red'}">{pnl:+.2f}%</div>
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
                            {positions_html}
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
                            {trades_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="card">
                    <h3 class="card-title">⚡ Today's Rebalances</h3>
                    {f"<div class='action-item buy'><div class='action-meta'><span class='action-ticker'>REBALANCED PORTFOLIO</span><span class='action-reason'>Equal-weight 18 picks</span></div><div class='action-val'>Cash: ${cash:.2f}</div></div>" if len(entry["rebalance_decisions"]) > 0 else "<div style='font-style:italic;color:var(--text-secondary)'>No trades today</div>"}
                </div>

                <div class="card">
                    <h3 class="card-title">🐺 Wolff Target Portfolio Weights</h3>
                    <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 15px;">
                        Allocations derived from Peter Wolff's Substack flagship fund updates.
                    </p>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        Equal weighting across 18 active picks: MSFT, META, NVDA, AVGO, AMD, PLTR, NOW, IREN, CIFR, WULF, NBIS, AMZN, ELV, LLY, BRK.B, BN, MELI, GRAB.
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

    # Text report
    txt_content = f"""📊 *Wolff Flagship Simulation Report — {date}* (SIMULATION)

*Simulation Portfolio Snapshot:*
💰 Total Virtual Value: ${total:.2f}
💵 Virtual Cash: ${cash:.2f}
📦 Virtual Positions: {len(entry["positions"])}
📈 vs. Start ($1,000): {pnl:+.2f}%

*Virtual Positions Detail:*
"""
    for pos in entry["positions"]:
        txt_content += f"• {pos['symbol']}: {pos['qty']:.6f} shares @ ${pos['avg_price']:.2f} → ${pos['current_price']:.2f} ({pos['pnl_pct']:+.2f}%)\n"
        
    txt_content += "\n*Today's Rebalances:*\n"
    for dec in decisions_list:
        txt_content += f"{dec}\n"
        
    txt_content += f"\n*Wolff Target Portfolio (from Substack/X):*\n• Equal weighted 18 active picks (target 5.0% each)\n"
    
    with open(os.path.join(SCRIPTS_DIR, "wolff_last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(txt_content)

def generate_report_3(entry):
    # ARK simulation report
    date = entry["date"]
    cash = entry["simulated_cash"]
    total = entry["total_portfolio_value"]
    pnl = ((total - 1000.0) / 1000.0) * 100.0
    
    positions_html = ""
    for pos in entry["positions"]:
        symbol = pos["symbol"]
        qty = pos["qty"]
        avg = pos["avg_price"]
        current = pos["current_price"]
        pos_pnl = pos["pnl_pct"]
        val = qty * current
        
        pnl_class = "text-green" if pos_pnl >= 0 else "text-red"
        pnl_sign = "+" if pos_pnl >= 0 else ""
        
        positions_html += f"""
        <tr>
            <td><strong>{symbol}</strong></td>
            <td>{qty:.6f}</td>
            <td>${avg:,.2f}</td>
            <td>${current:,.2f}</td>
            <td>${val:,.2f}</td>
            <td><span class="{pnl_class}">{pnl_sign}{pos_pnl:.2f}%</span></td>
            <td>{pos.get("ark_weight_pct", 0.0):.2f}%</td>
        </tr>
        """
        
    trades_html = ""
    decisions_list = []
    for d in entry["rebalance_decisions"]:
        symbol = d["symbol"]
        action = d["action"]
        amount = d["amount"]
        price = d["price"]
        qty = d["qty"]
        reason = d["reason"]
        
        action_color = "var(--green)" if action == "BUY" else "var(--red)"
        trades_html += f"""
        <tr>
            <td>{date}</td>
            <td><strong>{symbol}</strong></td>
            <td><span style="color: {action_color}">{action}</span></td>
            <td>{qty:.6f}</td>
            <td>${price:,.2f}</td>
            <td>${amount:,.2f}</td>
            <td>{reason}</td>
        </tr>
        """
        decisions_list.append(f"{'🟩' if action == 'BUY' else '🟥'} {action}: {symbol} × ${amount:.2f} at ${price:.2f} — {reason}")
        
    if not decisions_list:
        decisions_list.append("⏸ No simulated rebalances today.")
        trades_html = """
        <tr>
            <td colspan="7" style="text-align: center; color: var(--text-secondary); font-style: italic;">No trades executed today.</td>
        </tr>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARK Invest ARKK Simulation Report — {date}</title>
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
                <div class="timestamp">Market Day Run: Thursday, {date} | Iteration 5</div>
            </div>
            <div style="text-align: right">
                <span style="font-weight: 600; color: var(--accent);">📊 SIMULATION ENGINE</span>
            </div>
        </header>

        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Virtual Value</div>
                <div class="stat-value">${total:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Virtual Cash</div>
                <div class="stat-value">${cash:.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Return vs Start ($1000)</div>
                <div class="stat-value {'text-green' if pnl >= 0 else 'text-red'}">{pnl:+.2f}%</div>
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
                            {positions_html}
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
                            {trades_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <div>
                <div class="card">
                    <h3 class="card-title">⚡ Today's Rebalances</h3>
                    {f"<div class='action-item buy'><div class='action-meta'><span class='action-ticker'>REBALANCED PORTFOLIO</span><span class='action-reason'>Max 5 trades rate limit</span></div><div class='action-val'>Cash: ${cash:.2f}</div></div>" if len(entry["rebalance_decisions"]) > 0 else "<div style='font-style:italic;color:var(--text-secondary)'>No trades today</div>"}
                </div>

                <div class="card">
                    <h3 class="card-title">🦅 ARKK Top 10 Holdings</h3>
                    <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 15px;">
                        Disclosed positions and weighting inside Cathie Wood's ARKK ETF.
                    </p>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        Replicating ARKK holdings: TSLA, TEM, CRSP, AMD, HOOD, SHOP, ROKU, COIN, CRCL, TWST, PLTR, BEAM, TXG, AMZN.
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

    # Text report
    txt_content = f"""📊 *ARK Invest (ARKK) Simulation Report — {date}* (SIMULATION)

*Simulation Portfolio Snapshot:*
💰 Total Virtual Value: ${total:.2f}
💵 Virtual Cash: ${cash:.2f}
📦 Virtual Positions: {len(entry["positions"])}
📈 vs. Start ($1,000): {pnl:+.2f}%

*Virtual Positions Detail (mirroring ARKK):*
"""
    for pos in entry["positions"]:
        txt_content += f"• {pos['symbol']}: {pos['qty']:.6f} shares @ ${pos['avg_price']:.2f} → ${pos['current_price']:.2f} ({pos['pnl_pct']:+.2f}%) [ARKK Weight: {pos['ark_weight_pct']:.2f}%]\n"
        
    txt_content += "\n*Today's Rebalances:*\n"
    for dec in decisions_list:
        txt_content += f"{dec}\n"
        
    txt_content += f"\n*ARKK Top Holdings (as of {date}):*\n• TSLA (10.42%), TEM (4.98%), CRSP (4.90%), AMD (4.82%), HOOD (4.77%), BEAM (3.04%)\n"
    
    with open(os.path.join(SCRIPTS_DIR, "ark_last_report.txt"), 'w', encoding='utf-8') as f:
        f.write(txt_content)

def main():
    print("Loading journal records...")
    with open(os.path.join(MEMORY_DIR, "journal.json"), 'r', encoding='utf-8') as f:
        journal = json.load(f)
    with open(os.path.join(MEMORY_DIR, "wolff_journal.json"), 'r', encoding='utf-8') as f:
        wolff = json.load(f)
    with open(os.path.join(MEMORY_DIR, "ark_journal.json"), 'r', encoding='utf-8') as f:
        ark = json.load(f)
        
    latest_entry_1 = journal["entries"][-1]
    latest_entry_2 = wolff["entries"][-1]
    latest_entry_3 = ark["entries"][-1]
    
    print("Generating report 1 (Actual Portfolio)...")
    generate_report_1(latest_entry_1)
    
    print("Generating report 2 (Wolff Simulation)...")
    generate_report_2(latest_entry_2)
    
    print("Generating report 3 (ARK Simulation)...")
    generate_report_3(latest_entry_3)
    
    print("Reports generated successfully!")

if __name__ == "__main__":
    main()
