# indicators.py

import pandas_ta as ta
from utils import insert_indicator_signal
from datetime import datetime

def compute_all_indicators(df, cursor, symbol):
    try:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df.sort_index(inplace=True)

        scores = {
            "trend": 0,
            "momentum": 0,
            "volume": 0,
            "volatility": 0,
            "support_resistance": 0
        }

        # --- Trend Indicators ---
        df["ADX"] = ta.adx(df["high"], df["low"], df["close"], length=15)["ADX_15"]
        if df["ADX"].iloc[-1] > 25:
            scores["trend"] += 1
        elif df["ADX"].iloc[-1] < 20:
            scores["trend"] -= 1

        df["VWAP"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"])
        if df["close"].iloc[-1] > df["VWAP"].iloc[-1]:
            scores["trend"] += 1
        else:
            scores["trend"] -= 1

        # --- Momentum Indicators ---
        macd = ta.macd(df["close"], fast=18, slow=36, signal=9)
        if macd["MACD_18_36_9"].iloc[-1] > macd["MACDs_18_36_9"].iloc[-1]:
            scores["momentum"] += 1
        else:
            scores["momentum"] -= 1

        df["RSI"] = ta.rsi(df["close"], length=15)
        if df["RSI"].iloc[-1] < 30:
            scores["momentum"] += 1
        elif df["RSI"].iloc[-1] > 70:
            scores["momentum"] -= 1

        # --- Volume Indicators ---
        obv = ta.obv(df["close"], df["volume"])
        if obv.iloc[-1] > obv.iloc[-2]:
            scores["volume"] += 1
        else:
            scores["volume"] -= 1

        cho = ta.chaikin(df["high"], df["low"], df["close"], df["volume"], length=15)
        if cho.iloc[-1] > cho.iloc[-2]:
            scores["volume"] += 1
        else:
            scores["volume"] -= 1

        # --- Volatility Indicators ---
        bb = ta.bbands(df["close"], length=30, std=2)
        if df["close"].iloc[-1] < bb["BBL_30_2.0"].iloc[-1]:
            scores["volatility"] += 1
        elif df["close"].iloc[-1] > bb["BBU_30_2.0"].iloc[-1]:
            scores["volatility"] -= 1

        df["ATR"] = ta.atr(df["high"], df["low"], df["close"], length=15)
        if df["ATR"].iloc[-1] > df["ATR"].iloc[-2]:
            scores["volatility"] += 1
        else:
            scores["volatility"] -= 1

        # --- Support/Resistance Indicators ---
        # Simulate Fibonacci logic with rolling high/low
        recent_high = df["high"].rolling(window=21).max().iloc[-1]
        recent_low = df["low"].rolling(window=21).min().iloc[-1]
        fib_618 = recent_low + 0.618 * (recent_high - recent_low)

        if df["close"].iloc[-1] < fib_618:
            scores["support_resistance"] += 1
        else:
            scores["support_resistance"] -= 1

        # Gann Fan logic simulated with close vs avg HL
        gann_level = (df["high"] + df["low"]) / 2
        if df["close"].iloc[-1] > gann_level.iloc[-1]:
            scores["support_resistance"] += 1
        else:
            scores["support_resistance"] -= 1

        insert_indicator_signal(cursor, symbol, scores)

    except Exception as e:
        print(f"❌Error computing indicators for {symbol}: {e}")
