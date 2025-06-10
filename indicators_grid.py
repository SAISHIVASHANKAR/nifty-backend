# indicator_grid.py

from flask import Blueprint, render_template
import sqlite3

indicator_grid = Blueprint("indicator_grid", __name__)
DB_PATH = "nifty_stocks.db"

@indicator_grid.route("/grid2")
def grid2():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, trend, momentum, volume, volatility, support_resistance
        FROM indicator_signals
    """)
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        symbol, trend, momentum, volume, volatility, sr = row
        total_score = trend + momentum + volume + volatility + sr

        if total_score >= 8:
            color = "#006400"  # Strong Buy
        elif total_score >= 5:
            color = "#32CD32"  # Buy
        elif total_score >= 3:
            color = "#FFD700"  # Hold
        elif total_score >= 1:
            color = "#FF6347"  # Sell
        else:
            color = "#8B0000"  # Strong Sell

        data.append({
            "symbol": symbol,
            "trend": trend,
            "momentum": momentum,
            "volume": volume,
            "volatility": volatility,
            "sr": sr,
            "score": total_score,
            "color": color
        })

    return render_template("indicator_grid.html", data=data)
