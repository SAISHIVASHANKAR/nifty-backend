# run_indicators.py

from stocks import STOCKS
from utils import get_cached_df, insert_signal
from indicators import compute_all_indicators, generate_scores

def main():
    for symbol in STOCKS:
        try:
            df = get_cached_df(symbol)
            if df.empty or len(df) < 30:
                print(f"⚠️ Skipping {symbol}, insufficient data.")
                continue

            df = compute_all_indicators(df)
            scores = generate_scores(df)
            insert_signal(symbol, scores)

        except Exception as e:
            print(f"❌ Error in processing {symbol}: {e}")

if __name__ == "__main__":
    main()
