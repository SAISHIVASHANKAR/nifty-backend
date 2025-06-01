# fallback_bse.py

import pandas as pd
from datetime import datetime
from utils import insert_into_prices_table, symbol_has_data

# Placeholder for BSE fallback logic
def fetch_bse(symbol):
    if symbol_has_data(symbol):
        print(f"⏭️ Skipping {symbol}: already exists in DB.")
        return True

    try:
        print(f"🔹 Fetching BSE fallback data for {symbol} (stub logic)")
        today = datetime.today()
        data = {
            "Date": pd.date_range(end=today, periods=5),
            "Open": [200]*5,
            "High": [210]*5,
            "Low": [190]*5,
            "Close": [205]*5,
            "Volume": [2000]*5
        }
        df = pd.DataFrame(data)
        success = insert_into_prices_table(df, symbol)
        return success

    except Exception as e:
        print(f"BSE fetch failed for {symbol}: {e}")
        return False
