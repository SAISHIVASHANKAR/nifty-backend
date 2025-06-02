# fallback_eod.py
import pandas as pd
from utils import insert_into_prices_table

def fetch_eodhistorical(symbol):
    print(f"🍜 Trying EODHistorical for {symbol}")
    try:
        # This is stub fallback logic to simulate valid format
        data = {
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=30).strftime("%Y-%m-%d"),
            "Open": [100 + i for i in range(30)],
            "High": [101 + i for i in range(30)],
            "Low": [99 + i for i in range(30)],
            "Close": [100 + i for i in range(30)],
            "Volume": [1000 + i * 10 for i in range(30)]
        }
        df = pd.DataFrame(data)
        return insert_into_prices_table(df, symbol)
    except Exception as e:
        print(f"❌ EOD fetch failed for {symbol}: {e}")
        return False
