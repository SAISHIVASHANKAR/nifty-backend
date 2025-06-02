# indicators.py

import pandas as pd
import pandas_ta as ta
from utils import insert_indicator_signal

def compute_all_indicators(df, cursor, symbol):
    try:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        score = 0

        # Momentum
        macd = ta.macd(df["close"], fast=18, slow=36, signal=9)
        if macd is not None and not macd.isnull().values.any():
            if macd["MACD_18_36_9"].iloc[-1] > macd["MACDs_18_36_9"].iloc[-1]:
                score += 1
            else:
                score -= 1

        rsi = ta.rsi(df["close"], length=15)
        if rsi is not None and not rsi.isnull().values.any():
            if rsi.iloc[-1] > 50:
                score += 1
            else:
                score -= 1

        # Trend
        adx = ta.adx(df["high"], df["low"], df["close"], length=15)
        if adx is not None and not adx.isnull().values.any():
            if adx["ADX_15"].iloc[-1] > 25:
                score += 1
            else:
                score -= 1

        vwap = ta.vwap(df["high"], df["low"], df["close"], df["volume"], anchor="D")
        if vwap is not None and not vwap.isnull().values.any():
            if df["close"].iloc[-1] > vwap.iloc[-1]:
                score += 1
            else:
                score -= 1

        # Volume
        obv = ta.obv(df["close"], df["volume"])
        if obv is not None and not obv.isnull().values.any():
            if obv.iloc[-1] > obv.iloc[-2]:
                score += 1
            else:
                score -= 1

        chaikin = ta.adosc(df["high"], df["low"], df["close"], df["volume"], fast=3, slow=10)
        if chaikin is not None and not chaikin.isnull().values.any():
            if chaikin.iloc[-1] > 0:
                score += 1
            else:
                score -= 1

        # Volatility
        atr = ta.atr(df["high"], df["low"], df["close"], length=15)
        if atr is not None and not atr.isnull().values.any():
            if atr.iloc[-1] > atr.iloc[-2]:
                score += 1
            else:
                score -= 1

        bbands = ta.bbands(df["close"], length=30, std=2)
        if bbands is not None and not bbands.isnull().values.any():
            if df["close"].iloc[-1] > bbands["BBL_30_2.0"].iloc[-1]:
                score += 1
            else:
                score -= 1

        # Support/Resistance
        fib_support = df["close"].max() * 0.618
        if df["close"].iloc[-1] > fib_support:
            score += 1
        else:
            score -= 1

        gann_support = df["close"].mean()
        if df["close"].iloc[-1] > gann_support:
            score += 1
        else:
            score -= 1

        insert_indicator_signal(symbol, score, cursor)

    except Exception as e:
        print(f"❌ Error computing indicators for {symbol}: {e}")
