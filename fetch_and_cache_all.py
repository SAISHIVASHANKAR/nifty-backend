# fetch_and_cache_all.py

import os
import sqlite3
from utils import get_all_symbols, fetch_from_yf_fallback

# Define cache directory and database
CACHE_DIR = "/mnt/yf_cache"
DB_PATH = "nifty_stocks.db"

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    symbol TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (symbol, date)
)
""")
conn.commit()

# Get all stock symbols
symbols = get_all_symbols()

# Fetch and cache data
for symbol in symbols:
    print(f"📊 Fetching: {symbol}")
    try:
        df = fetch_from_yf_fallback(symbol)
        if df is None or df.empty:
            print(f"⚠️ Skipping {symbol}: No data fetched")
            continue

        # Save to cache CSV
        csv_path = os.path.join(CACHE_DIR, f"{symbol}.csv")
        df.to_csv(csv_path, index=False)

        # Insert into SQLite
        rows = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
        for row in rows:
            cursor.execute("""
                INSERT OR REPLACE INTO prices (symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [symbol, *row])
        conn.commit()

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")

conn.close()
print("✅ Done fetching EOD data.")
