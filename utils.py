# utils.py
import sqlite3
import pandas as pd

DB_PATH = "nifty_stocks.db"
SIGNAL_DB = "indicator_signals.db"

def get_cached_df(symbol):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT Date, Close, High, Low, Open, Volume
        FROM prices
        WHERE Symbol = ?
        ORDER BY Date ASC
    """
    df = pd.read_sql(query, conn, params=(symbol,), parse_dates=["Date"])
    conn.close()
    return df

def insert_indicator_signal(symbol, category, signal_type, score, count):
    conn = sqlite3.connect(SIGNAL_DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            Symbol TEXT,
            Category TEXT,
            Signal TEXT,
            Score INTEGER,
            Count INTEGER
        )
    ''')
    conn.execute('''
        INSERT INTO signals (Symbol, Category, Signal, Score, Count)
        VALUES (?, ?, ?, ?, ?)
    ''', (symbol, category, signal_type, score, count))
    conn.commit()
    conn.close()
