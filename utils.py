# utils.py

import sqlite3

def load_signals():
    conn = sqlite3.connect("indicator_signals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, trend, momentum, volume, volatility, support_resistance FROM signals")
    rows = cursor.fetchall()
    conn.close()
    return rows
