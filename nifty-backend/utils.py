# utils.py

import sqlite3

def load_signals():
    """Load signal data from the SQLite database and return as a list of dictionaries."""
    try:
        conn = sqlite3.connect("nifty_stocks.db")
        cursor = conn.cursor()

        cursor.execute("SELECT symbol, trend, momentum, volume, volatility, score FROM signals")
        rows = cursor.fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append({
                "symbol": row[0],
                "trend": row[1],
                "momentum": row[2],
                "volume": row[3],
                "volatility": row[4],
                "score": row[5]
            })

        return data

    except Exception as e:
        print(f"⚠️ Error loading signals from DB: {e}")
        return []
