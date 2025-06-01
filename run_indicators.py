# run_indicators.py
from stocks import STOCKS
from utils import get_cached_df
from indicators import compute_all_indicators

print("📊Running indicators and saving signals to indicator_signals.db")

for idx, symbol in enumerate(STOCKS.keys()):
    print(f"\n📈[{idx+1}/{len(STOCKS)}] Processing: {symbol}")
    try:
        df = get_cached_df(symbol)
        compute_all_indicators(symbol, df)
    except Exception as e:
        print(f"❌Error processing {symbol}: {e}")
