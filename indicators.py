# indicators.py

import pandas as pd
import numpy as np

def compute_rsi(df, period=15):
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(df, short=12, long=26, signal=9):
    short_ema = df["Close"].ewm(span=short, adjust=False).mean()
    long_ema = df["Close"].ewm(span=long, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line

def compute_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i - 1]:
            obv.append(obv[-1] + df["Volume"].iloc[i])
        elif df["Close"].iloc[i] < df["Close"].iloc[i - 1]:
            obv.append(obv[-1] - df["Volume"].iloc[i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)

def compute_bollinger_bands(df, period=30, std_dev=2):
    sma = df["Close"].rolling(window=period).mean()
    std = df["Close"].rolling(window=period).std()
    return sma + std_dev * std, sma - std_dev * std

def compute_adx(df, period=15):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    plus_dm = high.diff()
    minus_dm = low.diff()

    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = -minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).sum() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).sum() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    return dx.rolling(window=period).mean()

def compute_atr(df, period=15):
    tr1 = df["High"] - df["Low"]
    tr2 = abs(df["High"] - df["Close"].shift())
    tr3 = abs(df["Low"] - df["Close"].shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def compute_chaikin(df, period=15):
    adl = ((2 * df["Close"] - df["High"] - df["Low"]) / (df["High"] - df["Low"] + 1e-9)) * df["Volume"]
    return adl.ewm(span=period, adjust=False).mean()

def compute_vwap(df, period=10):
    tpv = ((df["High"] + df["Low"] + df["Close"]) / 3) * df["Volume"]
    return tpv.rolling(window=period).sum() / df["Volume"].rolling(window=period).sum()

def compute_fibonacci(df):
    max_price = df["High"].max()
    min_price = df["Low"].min()
    diff = max_price - min_price
    return {
        "0.0%": max_price,
        "23.6%": max_price - 0.236 * diff,
        "38.2%": max_price - 0.382 * diff,
        "50.0%": max_price - 0.500 * diff,
        "61.8%": max_price - 0.618 * diff,
        "100.0%": min_price
    }

def compute_gann_fan(df):
    base_price = df["Close"].iloc[0]
    slope = 1
    return pd.Series([base_price + slope * i for i in range(len(df))], index=df.index)

def compute_all_indicators(symbol, df):
    return {
        "symbol": symbol,
        "rsi": compute_rsi(df).iloc[-1],
        "macd": compute_macd(df).iloc[-1],
        "obv": compute_obv(df).iloc[-1],
        "bollinger_upper": compute_bollinger_bands(df)[0].iloc[-1],
        "bollinger_lower": compute_bollinger_bands(df)[1].iloc[-1],
        "adx": compute_adx(df).iloc[-1],
        "atr": compute_atr(df).iloc[-1],
        "chaikin": compute_chaikin(df).iloc[-1],
        "vwap": compute_vwap(df).iloc[-1],
        "gann": compute_gann_fan(df).iloc[-1],
        "fibonacci_50": compute_fibonacci(df)["50.0%"]
    }
