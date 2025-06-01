import os
import pandas as pd

CACHE_DIR = "/mnt/yf_cache"

def load_price_data(symbol):
    file_path = os.path.join(CACHE_DIR, f"{symbol}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Price file not found for {symbol}: {file_path}")
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df = df.dropna()
    return df

def insert_indicator_signal(cursor, symbol, trend, momentum, volume, volatility, support_resistance):
    cursor.execute("""
        INSERT OR REPLACE INTO signals 
        (symbol, trend, momentum, volume, volatility, support_resistance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (symbol, trend, momentum, volume, volatility, support_resistance))
