# run_indicators.py

from stocks import STOCKS
from utils import get_cached_df, insert_signal
from indicators import compute_all_indicators, generate_scores

def main():
    for symbol in STOCKS:
        print(f"\n📈 Processing {symbol}")
        try:
            df = get_cached_df(symbol)
            if df.empty:
                print(f"⚠️ Skipping {symbol} - No data found.")
                continue
            if len(df) < 30:
                print(f"⚠️ Skipping {symbol} - Not enough data ({len(df)} rows).")
                continue

            try:
                df = compute_all_indicators(df)
            except Exception as e:
                print(f"❌ compute_all_indicators() failed for {symbol}: {e}")
                continue

            try:
                scores = generate_scores(df)
            except Exception as e:
                print(f"❌ generate_scores() failed for {symbol}: {e}")
                continue

            try:
                insert_signal(symbol, scores)
            except Exception as e:
                print(f"❌ insert_signal() failed for {symbol}: {e}")
                continue

        except Exception as e:
            print(f"❌ Outer error in processing {symbol}: {e}")

if __name__ == "__main__":
    main()
