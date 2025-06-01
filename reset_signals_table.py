import sqlite3

conn = sqlite3.connect("indicator_signals.db")
c = conn.cursor()

# Drop old table if it exists
c.execute("DROP TABLE IF EXISTS signals")

# Recreate the table with all 7 columns
c.execute("""
    CREATE TABLE signals (
        symbol TEXT PRIMARY KEY,
        trend INTEGER,
        momentum INTEGER,
        volume INTEGER,
        volatility INTEGER,
        support_resistance INTEGER,
        count INTEGER
    )
""")

conn.commit()
conn.close()
print("✅ signals table reset with count column.")
