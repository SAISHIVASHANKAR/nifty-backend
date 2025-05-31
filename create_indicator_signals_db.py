import sqlite3

conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    symbol TEXT PRIMARY KEY,
    trend TEXT,
    momentum TEXT,
    volume TEXT,
    volatility TEXT,
    support_resistance TEXT
)
""")

conn.commit()
conn.close()
print("✅ Created signals table in indicator_signals.db")
