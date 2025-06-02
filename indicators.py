# indicators.py

import pandas as pd
import numpy as np
from ta.trend import ADXIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from utils import insert_indicator_signal

def compute_all_indicators(symbol, df, cursor):
    try:
        df = df.copy()
        df["Date"] = pd.to_datetime(df["date"])

        # Ensure necessary columns exist
        if len(df) < 50:
            print(f"⚠️ Not enough data for {symbol}")
            return

        # === TREND ===
        adx = ADXIndicator(df["high"], df["low"], df["close"], window=15).adx()
        df["ADX"] = adx
        trend_score = 1 if df["ADX"].iloc[-1] > 20 else -1

        df["VWAP"] = (df["volume"] * (df["high"] + df["low"] + df["close"]) / 3).cumsum() / df["volume"].cumsum()
        trend_score += 1 if df["close"].iloc[-1] > df["VWAP"].iloc[-1] else -1

        # === MOMENTUM ===
        macd = MACD(df["close"], window_slow=36, window_fast=18, window_sign=9)
        df["MACD"] = macd.macd()
        df["MACD_signal"] = macd.macd_signal()
        momentum_score = 1 if df["MACD"].iloc[-1] > df["MACD_signal"].iloc[-1] else -1

        rsi = RSIIndicator(df["close"], window=15).rsi()
        df["RSI"] = rsi
        momentum_score += 1 if df["RSI"].iloc[-1] > 50 else -1

        # === VOLUME ===
        obv = OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()
        df["OBV"] = obv
        obv_mean = obv.rolling(window=20).mean()
        volume_score = 1 if obv.iloc[-1] > obv_mean.iloc[-1] else -1

        df["Chaikin"] = ((2 * df["close"] - df["high"] - df["low"]) / (df["high"] - df["low"] + 1e-9)) * df["volume"]
        chaikin_mean = df["Chaikin"].rolling(window=15).mean()
        volume_score += 1 if df["Chaikin"].iloc[-1] > chaikin_mean.iloc[-1] else -1

        # === VOLATILITY ===
        atr = AverageTrueRange(df["high"], df["low"], df["close"], window=15).average_true_range()
        df["ATR"] = atr
        atr_mean = atr.rolling(window=20).mean()
        volatility_score = 1 if df["ATR"].iloc[-1] > atr_mean.iloc[-1] else -1

        boll = BollingerBands(df["close"], window=30, window_dev=2)
        upper = boll.bollinger_hband()
        lower = boll.bollinger_lband()
        close = df["close"].iloc[-1]
        if close > upper.iloc[-1]:
            volatility_score += 1
        elif close < lower.iloc[-1]:
            volatility_score -= 1

        # === SUPPORT / RESISTANCE ===
        high_price = df["high"].max()
        low_price = df["low"].min()
        diff = high_price - low_price
        level_1_1 = low_price + 0.125 * diff
        level_2_1 = low_price + 0.25 * diff
        level_3_1 = low_price + 0.375 * diff
        level_4_1 = low_price + 0.5 * diff
        level_5_1 = low_price + 0.625 * diff

        support_resistance_score = 0
        if close > level_5_1:
            support_resistance_score += 2
        elif close > level_4_1:
            support_resistance_score += 1
        elif close < level_2_1:
            support_resistance_score -= 1
        elif close < level_1_1:
            support_resistance_score -= 2

        gann_line = low_price + 0.5 * diff
        support_resistance_score += 1 if close > gann_line else -1

        # === FINAL INSERT ===
        insert_indicator_signal(cursor, symbol,
                                trend_score, momentum_score,
                                volume_score, volatility_score,
                                support_resistance_score)

    except Exception as e:
        print(f"Error computing indicators for {symbol}: {e}")
