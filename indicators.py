# indicators.py

import pandas as pd
import pandas_ta as ta

def compute_all_indicators(df):
    scores = {
        "trend": 0,
        "momentum": 0,
        "volume": 0,
        "volatility": 0,
        "support_resistance": 0
    }

    try:
        # Ensure DataFrame is sorted by date
        df = df.sort_values("date")
        close = df["close"]
        high = df["high"]
        low = df["low"]
        volume = df["volume"]

        # === Trend Indicators ===
        df["ADX"] = ta.adx(high, low, close, length=15)["ADX_15"]
        if df["ADX"].iloc[-1] > 25:
            scores["trend"] += 1
        else:
            scores["trend"] -= 1

        df["VWAP"] = ta.vwap(high, low, close, volume=volume)
        if close.iloc[-1] > df["VWAP"].iloc[-1]:
            scores["trend"] += 1
        else:
            scores["trend"] -= 1

        # === Momentum Indicators ===
        macd = ta.macd(close, fast=18, slow=36, signal=9)
        if macd["MACD_18_36_9"].iloc[-1] > macd["MACDs_18_36_9"].iloc[-1]:
            scores["momentum"] += 1
        else:
            scores["momentum"] -= 1

        df["RSI"] = ta.rsi(close, length=15)
        if df["RSI"].iloc[-1] > 50:
            scores["momentum"] += 1
        else:
            scores["momentum"] -= 1

        # === Volume Indicators ===
        obv = ta.obv(close, volume)
        if obv.diff().iloc[-1] > 0:
            scores["volume"] += 1
        else:
            scores["volume"] -= 1

        chaikin = ta.chaikin(high, low, close, volume, fast=3, slow=10)
        if chaikin.iloc[-1] > 0:
            scores["volume"] += 1
        else:
            scores["volume"] -= 1

        # === Volatility Indicators ===
        df["ATR"] = ta.atr(high, low, close, length=15)
        if df["ATR"].iloc[-1] > df["ATR"].mean():
            scores["volatility"] += 1
        else:
            scores["volatility"] -= 1

        bb = ta.bbands(close, length=30, std=2)
        if close.iloc[-1] < bb["BBL_30_2.0"].iloc[-1]:
            scores["volatility"] -= 1
        elif close.iloc[-1] > bb["BBU_30_2.0"].iloc[-1]:
            scores["volatility"] += 1

        # === Support/Resistance ===
        # Gann Fan: if price above 1:1 angle (simulated with moving average)
        df["GannFan"] = ta.sma(close, length=30)
        if close.iloc[-1] > df["GannFan"].iloc[-1]:
            scores["support_resistance"] += 1
        else:
            scores["support_resistance"] -= 1

        # Fibonacci: simplified rule — check retracement level zone
        recent_high = high.iloc[-20:].max()
        recent_low = low.iloc[-20:].min()
        fib_618 = recent_high - 0.618 * (recent_high - recent_low)
        if close.iloc[-1] > fib_618:
            scores["support_resistance"] += 1
        else:
            scores["support_resistance"] -= 1

    except Exception as e:
        print(f"Indicator computation error: {e}")

    return scores
