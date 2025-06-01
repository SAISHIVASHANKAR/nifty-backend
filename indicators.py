# indicators.py

import pandas as pd
import numpy as np

def compute_rsi(df, period=15):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_macd(df, fast=12, slow=26, signal=9):
    fast_ema = df["Close"].ewm(span=fast, adjust=False).mean()
    slow_ema = df["Close"].ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd - signal_line

def compute_adx(df, period=15):
    plus_dm = df["High"].diff()
    minus_dm = df["Low"].diff().abs()
    tr1 = df["High"] - df["Low"]
    tr2 = abs(df["High"] - df["Close"].shift())
    tr3 = abs(df["Low"] - df["Close"].shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def compute_atr(df, period=15):
    tr = df["High"].combine(df["Low"], max) - df["Low"].combine(df["High"], min)
    return tr.rolling(window=period).mean()

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

def compute_vwap(df, period=10):
    pv = (df["Close"] * df["Volume"]).rolling(window=period).sum()
    v = df["Volume"].rolling(window=period).sum()
    return pv / v

def compute_chaikin(df, period=15):
    adl = ((2 * df["Close"] - df["High"] - df["Low"]) / (df["High"] - df["Low"]) * df["Volume"]).fillna(0)
    return adl.ewm(span=period, adjust=False).mean()

def compute_bollinger_bands(df, period=30):
    sma = df["Close"].rolling(window=period).mean()
    std = df["Close"].rolling(window=period).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    return upper, lower

def compute_fibonacci(df):
    max_price = df["Close"].max()
    min_price = df["Close"].min()
    diff = max_price - min_price
    levels = [0.236, 0.382, 0.618]
    return [max_price - (diff * lvl) for lvl in levels]

def compute_gann(df):
    return df["Close"] + (df["Close"] * 0.125)

def compute_all_indicators(symbol, df):
    try:
        rsi = compute_rsi(df).iloc[-1]
        macd = compute_macd(df).iloc[-1]
        adx = compute_adx(df).iloc[-1]
        atr = compute_atr(df).iloc[-1]
        obv = compute_obv(df).iloc[-1]
        vwap = compute_vwap(df).iloc[-1]
        chaikin = compute_chaikin(df).iloc[-1]
        upper, lower = compute_bollinger_bands(df)
        boll = (df["Close"].iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1])
        fibs = compute_fibonacci(df)
        gann = compute_gann(df).iloc[-1]

        trend = int((macd > 0) + (adx > 20) + (vwap > df["Close"].iloc[-1]))
        momentum = int((rsi > 50) + (macd > 0))
        volume = int((obv.diff().iloc[-1] > 0) + (chaikin.diff().iloc[-1] > 0))
        volatility = int((atr > atr.mean()) + (boll > 0.5))
        support_resistance = int((df["Close"].iloc[-1] > fibs[1]) + (df["Close"].iloc[-1] > gann))

        return trend, momentum, volume, volatility, support_resistance

    except Exception as e:
        print(f"❌ Failed computing indicators for {symbol}: {e}")
        return None
