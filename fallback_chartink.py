# fallback_chartink.py

import pandas as pd
from datetime import datetime
from utils import insert_into_prices_table, symbol_has_data

def fetch_chartink(symbol):
    if symbol_has_data(symbol):
        print(f"⏭️ Skipping {symbol}: already exists in DB.")
        return True

    try:
        print(f"🔹 Fetching Chartink fallback data for {symbol} (stub logic)")
        today = datetime.today()
        data = {
            "Date": pd.date_range(end=today, periods=5),
            "Open": [100] * 5,
            "High": [105] * 5,
            "Low": [95] * 5,
            "Close": [102] * 5,
            "Volume": [1000] * 5
        }
        df = pd.DataFrame(data)
        success = insert_into_prices_table(df, symbol)
        return success

    except Exception as e:
        print(f"Chartink fetch failed for {symbol}: {e}")
        return False
