import sqlite3
import pandas as pd

# ✅ Load EOD prices for a symbol from SQLite
def get_cached_df(symbol):
    conn = sqlite3.connect("nifty_stocks.db")
    query = f"SELECT Date, Close, High, Low, Open, Volume FROM prices WHERE Symbol = ?"
    try:
        df = pd.read_sql(query, conn, params=(symbol,), parse_dates=["Date"])
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(f"❌ Failed to load cached data for {symbol}: {e}")
        return None
    finally:
        conn.close()

# ✅ Write EOD prices into SQLite
def insert_into_prices_table(df, symbol):
    try:
        conn = sqlite3.connect("nifty_stocks.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                Symbol TEXT,
                Date TEXT,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Volume REAL,
                PRIMARY KEY (Symbol, Date)
            )
            """
        )
        df["Symbol"] = symbol
        df.to_sql("prices", conn, if_exists="append", index=False)
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ DB insert error for {symbol}: {e}")
        return False
    finally:
        conn.close()

# ✅ Save technical indicator scores
def insert_indicator_signal(symbol, trend, momentum, volume, volatility, support_resistance, total_score):
    conn = sqlite3.connect("nifty_stocks.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS indicator_signals (
            Symbol TEXT PRIMARY KEY,
            Trend INTEGER,
            Momentum INTEGER,
            Volume INTEGER,
            Volatility INTEGER,
            SupportResistance INTEGER,
            TotalScore INTEGER
        )
        """
    )
    cursor.execute(
        """
        INSERT OR REPLACE INTO indicator_signals
        (Symbol, Trend, Momentum, Volume, Volatility, SupportResistance, TotalScore)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (symbol, trend, momentum, volume, volatility, support_resistance, total_score)
    )
    conn.commit()
    conn.close()
