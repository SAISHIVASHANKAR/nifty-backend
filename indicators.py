# indicators.py
import pandas as pd
from utils import insert_indicator_signal

def compute_all_indicators(symbol, df):
    try:
        if df is None or df.empty or len(df.columns) < 6:
            print(f"⚠️Skipping {symbol}: Missing required columns or empty")
            return

        score = 0
        count = 0

        # Example placeholder logic
        if df["Close"].iloc[-1] > df["Close"].mean():
            score += 5
            count += 1

        if df["Volume"].iloc[-1] > df["Volume"].mean():
            score += 2
            count += 1

        insert_indicator_signal(symbol, "trend", "buy", score, count)
        print(f"✅{symbol} inserted: Total Score = {score}")
    except Exception as e:
        print(f"❌Failed to insert signal for {symbol}: {e}")
