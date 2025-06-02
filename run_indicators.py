# run_indicators.py

from stocks import STOCKS
from utils import get_cached_df, insert_indicator_signal
from indicators import compute_all_indicators

for symbol in STOCKS:
    df = get_cached_df(symbol)
    if df is None or df.empty or len(df) < 50:
        print(f"Skipping {symbol} due to insufficient or missing data.")
        continue

    try:
        scores = compute_all_indicators(df)
        insert_indicator_signal(symbol, scores)
        print(f"✅ Indicators for {symbol} inserted.")
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")
