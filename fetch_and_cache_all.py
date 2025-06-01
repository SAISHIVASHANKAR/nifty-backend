from stocks import STOCKS
from fetch_from_yf import fetch_yf
from utils import insert_into_prices_table
import pandas as pd

def fetch_with_fallbacks(symbol):
    for y in range(8, 0, -1):
        df = fetch_yf(symbol, years=y)
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
    return pd.DataFrame()

def main():
    for idx, symbol in enumerate(list(STOCKS.keys())[:3]):  # 🔁 Limit to 3 for testing
        print(f"\n[{idx+1}/3] Processing: {symbol}")
        df = fetch_with_fallbacks(symbol)
        insert_into_prices_table(df, symbol)

if __name__ == "__main__":
    main()
