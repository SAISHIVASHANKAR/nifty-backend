# reset_signals_table.py

import sqlite3

conn = sqlite3.connect("nifty_stocks.db")
c = conn.cursor()

# Drop old table if exists
c.execute("DROP TABLE IF EXISTS indicator_signals")

# Create new table with correct columns
c.execute("""
CREATE TABLE indicator_signals (
    symbol TEXT,
    trend INTEGER,
    momentum INTEGER,
    volume INTEGER,
    volatility INTEGER,
    support_resistance INTEGER
)
""")

conn.commit()
conn.close()
print("✅ indicator_signals table reset and ready!")
