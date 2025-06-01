# utils.py

import os
import pandas as pd

def get_cached_df(symbol):
    path = f"/mnt/yf_cache/{symbol}.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No cache for {symbol}")
    df = pd.read_csv(path)

    # Convert all price/volume columns to numeric in case of bad formatting
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop any rows with NaN values to avoid processing errors
    df.dropna(inplace=True)
    return df
