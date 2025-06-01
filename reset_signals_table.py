# reset_signals_table.py
# This script resets the 'signals' table in indicator_signals.db with all 7 required columns

import sqlite3

# Connect to the existing SQLite database
conn = sqlite3.connect("indicator_signals.db")
cursor = conn.cursor()

# Drop the existing table if it exists
cursor.execute("DROP TABLE IF EXISTS signals")

# Recreate the table with 7 fields including 'count'
cursor.execute("""
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

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ signals table recreated with all 7 columns including 'count'.")
