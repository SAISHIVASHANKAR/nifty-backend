# fallback_chartink.py

from utils import insert_into_prices_table
import pandas as pd

# Stub implementation (no real Chartink scraping)
def fetch_chartink(symbol):
    try:
        print(f"☕️Fetching Chartink fallback data for {symbol} (stub logic)")

        # Fake fallback data structure with proper column names
        data = {
            "date": pd.date_range(end=pd.Timestamp.today(), periods=10),
            "open": [100 + i for i in range(10)],
            "high": [105 + i for i in range(10)],
            "low": [95 + i for i in range(10)],
            "close": [102 + i for i in range(10)],
            "volume": [100000 + i * 1000 for i in range(10)]
        }
        df = pd.DataFrame(data)

        inserted = insert_into_prices_table(df, symbol)
        return inserted

    except Exception as e:
        print(f"Chartink fallback failed for {symbol}: {e}")
        return False
