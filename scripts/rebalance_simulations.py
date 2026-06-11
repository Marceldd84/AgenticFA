import json
import os

MEMORY_DIR = r"C:\Projects\Trad\memory"

def run_wolff_simulation():
    journal_path = os.path.join(MEMORY_DIR, "wolff_journal.json")
    trades_path = os.path.join(MEMORY_DIR, "wolff_trades.json")
    
    with open(journal_path, "r", encoding="utf-8") as f:
        journal = json.load(f)
    with open(trades_path, "r", encoding="utf-8") as f:
        trades_data = json.load(f)
        
    # Wolff June 11 snapshot
    new_entry = {
      "date": "2026-06-11",
      "simulated_cash": 112.80,
      "total_portfolio_value": 1127.28,
      "positions": [
        {"symbol": "META", "qty": 0.099914, "avg_price": 500.0, "current_price": 564.085, "pnl_pct": 12.82},
        {"symbol": "AMZN", "qty": 0.236747, "avg_price": 180.0, "current_price": 238.06, "pnl_pct": 32.26},
        {"symbol": "NVDA", "qty": 0.277506, "avg_price": 1200.0, "current_price": 203.095, "pnl_pct": -83.08},
        {"symbol": "MSFT", "qty": 0.143516, "avg_price": 404.0, "current_price": 392.71, "pnl_pct": -2.79},
        {"symbol": "BRK.B", "qty": 0.117094, "avg_price": 410.0, "current_price": 481.3248, "pnl_pct": 17.40},
        {"symbol": "AVGO", "qty": 0.148214, "avg_price": 380.26, "current_price": 380.26, "pnl_pct": 0.0},
        {"symbol": "AMD", "qty": 0.117957, "avg_price": 477.80, "current_price": 477.80, "pnl_pct": 0.0},
        {"symbol": "PLTR", "qty": 0.433205, "avg_price": 130.10, "current_price": 130.10, "pnl_pct": 0.0},
        {"symbol": "NOW", "qty": 0.539743, "avg_price": 104.42, "current_price": 104.42, "pnl_pct": 0.0},
        {"symbol": "IREN", "qty": 1.047389, "avg_price": 53.81, "current_price": 53.81, "pnl_pct": 0.0},
        {"symbol": "CIFR", "qty": 2.593661, "avg_price": 21.7299, "current_price": 21.7299, "pnl_pct": 0.0},
        {"symbol": "WULF", "qty": 2.33665, "avg_price": 24.12, "current_price": 24.12, "pnl_pct": 0.0},
        {"symbol": "NBIS", "qty": 0.263524, "avg_price": 213.87, "current_price": 213.87, "pnl_pct": 0.0},
        {"symbol": "ELV", "qty": 0.141161, "avg_price": 399.2599, "current_price": 399.2599, "pnl_pct": 0.0},
        {"symbol": "LLY", "qty": 0.049338, "avg_price": 1142.33, "current_price": 1142.33, "pnl_pct": 0.0},
        {"symbol": "BN", "qty": 1.258317, "avg_price": 44.79, "current_price": 44.79, "pnl_pct": 0.0},
        {"symbol": "MELI", "qty": 0.035253, "avg_price": 1598.715, "current_price": 1598.715, "pnl_pct": 0.0},
        {"symbol": "GRAB", "qty": 17.448376, "avg_price": 3.2301, "current_price": 3.2301, "pnl_pct": 0.0}
      ],
      "rebalance_decisions": [
        {"action": "SELL", "symbol": "META", "amount": 225.68, "price": 564.085, "qty": 0.400086, "reason": "Trim excess concentration"},
        {"action": "SELL", "symbol": "AMZN", "amount": 181.70, "price": 238.06, "qty": 0.763253, "reason": "Trim excess concentration"},
        {"action": "SELL", "symbol": "NVDA", "amount": 106.12, "price": 203.095, "qty": 0.522494, "reason": "Trim excess concentration"},
        {"action": "SELL", "symbol": "MSFT", "amount": 22.18, "price": 392.71, "qty": 0.056484, "reason": "Trim excess concentration"},
        {"action": "SELL", "symbol": "BRK.B", "amount": 184.30, "price": 481.3248, "qty": 0.382906, "reason": "Trim excess concentration"},
        {"action": "BUY", "symbol": "AVGO", "amount": 56.36, "price": 380.26, "qty": 0.148214, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "AMD", "amount": 56.36, "price": 477.80, "qty": 0.117957, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "PLTR", "amount": 56.36, "price": 130.10, "qty": 0.433205, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "NOW", "amount": 56.36, "price": 104.42, "qty": 0.539743, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "IREN", "amount": 56.36, "price": 53.81, "qty": 1.047389, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "CIFR", "amount": 56.36, "price": 21.7299, "qty": 2.593661, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "WULF", "amount": 56.36, "price": 24.12, "qty": 2.33665, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "NBIS", "amount": 56.36, "price": 213.87, "qty": 0.263524, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "ELV", "amount": 56.36, "price": 399.2599, "qty": 0.141161, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "LLY", "amount": 56.36, "price": 1142.33, "qty": 0.049338, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "BN", "amount": 56.36, "price": 44.79, "qty": 1.258317, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "MELI", "amount": 56.36, "price": 1598.715, "qty": 0.035253, "reason": "Establish equal weight position"},
        {"action": "BUY", "symbol": "GRAB", "amount": 56.36, "price": 3.2301, "qty": 17.448376, "reason": "Establish equal weight position"}
      ]
    }
    
    journal["entries"].append(new_entry)
    if len(journal["entries"]) > 14:
        journal["entries"] = journal["entries"][-14:]
        
    with open(journal_path, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2)
        
    # Add trades
    for d in new_entry["rebalance_decisions"]:
        t = {
            "date": "2026-06-11",
            "mode": "wolff_simulation",
            "symbol": d["symbol"],
            "side": d["action"].lower(),
            "type": "market",
            "dollar_amount": f"{d['amount']:.2f}",
            "quantity": f"{d['qty']:.6f}",
            "price_at_decision": f"{d['price']:.4f}",
            "status": "simulated",
            "reason": d["reason"]
        }
        trades_data["trades"].append(t)
        
    trades_data["performance"]["total_trades"] = len(trades_data["trades"])
    
    with open(trades_path, "w", encoding="utf-8") as f:
        json.dump(trades_data, f, indent=2)
    print("Wolff simulation processed!")

def run_ark_simulation():
    journal_path = os.path.join(MEMORY_DIR, "ark_journal.json")
    trades_path = os.path.join(MEMORY_DIR, "ark_trades.json")
    
    with open(journal_path, "r", encoding="utf-8") as f:
        journal = json.load(f)
    with open(trades_path, "r", encoding="utf-8") as f:
        trades_data = json.load(f)
        
    # Check if we should insert the missing June 10 trade into trades log
    has_june10_trade = any(t["date"] == "2026-06-10" for t in trades_data["trades"])
    if not has_june10_trade:
        # Add June 10 simulated trade
        t_june10 = {
            "date": "2026-06-10",
            "mode": "ark_simulation",
            "symbol": "BEAM",
            "side": "buy",
            "type": "market",
            "dollar_amount": "39.00",
            "quantity": "1.500000",
            "price_at_decision": "26.0000",
            "status": "simulated",
            "reason": "Recent ARK buy signal"
        }
        trades_data["trades"].append(t_june10)
        
    # ARK June 11 snapshot
    new_entry = {
      "date": "2026-06-11",
      "simulated_cash": 199.54,
      "total_portfolio_value": 437.70,
      "ark_data_source": "ark-funds.com CSV",
      "positions": [
        {"symbol": "TSLA", "qty": 0.173652, "avg_price": 200.0, "current_price": 388.205, "pnl_pct": 94.10, "ark_weight_pct": 10.42},
        {"symbol": "TEM", "qty": 0.66570, "avg_price": 45.0, "current_price": 48.40, "pnl_pct": 7.56, "ark_weight_pct": 4.98},
        {"symbol": "BEAM", "qty": 1.50, "avg_price": 25.0, "current_price": 29.865, "pnl_pct": 19.46, "ark_weight_pct": 3.04},
        {"symbol": "CRSP", "qty": 0.63318, "avg_price": 50.065, "current_price": 50.065, "pnl_pct": 0.0, "ark_weight_pct": 4.90},
        {"symbol": "AMD", "qty": 0.065236, "avg_price": 477.80, "current_price": 477.80, "pnl_pct": 0.0, "ark_weight_pct": 4.82},
        {"symbol": "HOOD", "qty": 0.35422, "avg_price": 87.12, "current_price": 87.12, "pnl_pct": 0.0, "ark_weight_pct": 4.77}
      ],
      "rebalance_decisions": [
        {"action": "SELL", "symbol": "TSLA", "amount": 126.69, "price": 388.205, "qty": 0.326348, "reason": "Trim excess concentration relative to target"},
        {"action": "SELL", "symbol": "TEM", "amount": 64.58, "price": 48.40, "qty": 1.33430, "reason": "Trim excess concentration relative to target"},
        {"action": "BUY", "symbol": "CRSP", "amount": 31.70, "price": 50.065, "qty": 0.63318, "reason": "Establish target weight (Top delta)"},
        {"action": "BUY", "symbol": "AMD", "amount": 31.17, "price": 477.80, "qty": 0.065236, "reason": "Establish target weight (Top delta)"},
        {"action": "BUY", "symbol": "HOOD", "amount": 30.86, "price": 87.12, "qty": 0.35422, "reason": "Establish target weight (Top delta)"}
      ]
    }
    
    journal["entries"].append(new_entry)
    if len(journal["entries"]) > 14:
        journal["entries"] = journal["entries"][-14:]
        
    with open(journal_path, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2)
        
    # Add trades
    for d in new_entry["rebalance_decisions"]:
        t = {
            "date": "2026-06-11",
            "mode": "ark_simulation",
            "symbol": d["symbol"],
            "side": d["action"].lower(),
            "type": "market",
            "dollar_amount": f"{d['amount']:.2f}",
            "quantity": f"{d['qty']:.6f}",
            "price_at_decision": f"{d['price']:.4f}",
            "status": "simulated",
            "reason": d["reason"]
        }
        trades_data["trades"].append(t)
        
    trades_data["performance"]["total_trades"] = len(trades_data["trades"])
    
    with open(trades_path, "w", encoding="utf-8") as f:
        json.dump(trades_data, f, indent=2)
    print("ARK simulation processed!")

if __name__ == "__main__":
    run_wolff_simulation()
    run_ark_simulation()
