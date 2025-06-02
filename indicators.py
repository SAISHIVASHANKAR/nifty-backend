# indicators.py

import pandas as pd
import talib

def compute_all_indicators(df, cursor, symbol):
    try:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        volume = df["volume"].values

        # Indicator Scores
        trend_score = 0
        momentum_score = 0
        volume_score = 0
        volatility_score = 0
        support_resistance_score = 0

        # ----- Trend -----
        adx = talib.ADX(high, low, close, timeperiod=15)
        if adx.iloc[-1] > 25:
            trend_score += 1
        elif adx.iloc[-1] < 20:
            trend_score -= 1

        vwap = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
        if df["close"].iloc[-1] > vwap.iloc[-1]:
            trend_score += 1
        else:
            trend_score -= 1

        # ----- Momentum -----
        macd, signal, _ = talib.MACD(close, fastperiod=18, slowperiod=36, signalperiod=9)
        if macd.iloc[-1] > signal.iloc[-1]:
            momentum_score += 1
        else:
            momentum_score -= 1

        rsi = talib.RSI(close, timeperiod=15)
        if rsi.iloc[-1] < 30:
            momentum_score += 1
        elif rsi.iloc[-1] > 70:
            momentum_score -= 1

        # ----- Volume -----
        obv = talib.OBV(close, volume)
        if obv.iloc[-1] > obv.iloc[-2]:
            volume_score += 1
        else:
            volume_score -= 1

        chaikin = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        if chaikin.iloc[-1] > 0:
            volume_score += 1
        else:
            volume_score -= 1

        # ----- Volatility -----
        atr = talib.ATR(high, low, close, timeperiod=15)
        if atr.iloc[-1] > atr.iloc[-20:-1].mean():
            volatility_score += 1
        else:
            volatility_score -= 1

        upper, middle, lower = talib.BBANDS(close, timeperiod=30, nbdevup=2, nbdevdn=2)
        if close[-1] < lower[-1]:
            volatility_score += 1
        elif close[-1] > upper[-1]:
            volatility_score -= 1

        # ----- Support/Resistance -----
        close_today = close[-1]
        close_yesterday = close[-2]
        midpoint = (high[-2] + low[-2]) / 2
        if close_today > midpoint and close_today > close_yesterday:
            support_resistance_score += 1
        elif close_today < midpoint and close_today < close_yesterday:
            support_resistance_score -= 1

        # Gann Fan (Stub logic)
        if close_today > close.mean():
            support_resistance_score += 1
        else:
            support_resistance_score -= 1

        cursor.execute("""
            INSERT INTO indicator_signals
            (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, trend_score, momentum_score, volume_score, volatility_score, support_resistance_score))

        return True

    except Exception as e:
        print(f"❌ Error computing indicators for {symbol}: {e}")
        return False
