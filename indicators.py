# indicators.py

import pandas as pd
import pandas_ta as ta
from utils import insert_indicator_signal

def compute_all_indicators(df, cursor):
    if df.empty:
        print("⚠️ DataFrame is empty. Skipping...")
        return

    try:
        # ✅ Ensure datetime index for VWAP and time-based indicators
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.sort_index()

        signals = {
            "trend": 0,
            "momentum": 0,
            "volume": 0,
            "volatility": 0,
            "support_resistance": 0
        }

        # ============================ TREND =============================
        # ✅ 1. ADX(15)
        adx = ta.adx(df['high'], df['low'], df['close'], length=15)
        if adx is not None and not adx.empty and adx.iloc[-1]['ADX_15'] > 25:
            signals["trend"] += 1

        # ✅ 2. VWAP(10)
        vwap = ta.vwap(df['high'], df['low'], df['close'], df['volume'], anchor='D')
        if vwap is not None and not vwap.empty and df['close'].iloc[-1] > vwap.iloc[-1]:
            signals["trend"] += 1

        # ========================== MOMENTUM ============================
        # ✅ 3. MACD (18,36,9)
        macd = ta.macd(df['close'], fast=18, slow=36, signal=9)
        if macd is not None and not macd.empty and macd.iloc[-1]['MACD_18_36_9'] > macd.iloc[-1]['MACDs_18_36_9']:
            signals["momentum"] += 1

        # ✅ 4. RSI(15)
        rsi = ta.rsi(df['close'], length=15)
        if rsi is not None and not rsi.empty and rsi.iloc[-1] > 50:
            signals["momentum"] += 1

        # ============================ VOLUME ============================
        # ✅ 5. Chaikin Oscillator(15)
        chaikin = ta.adosc(df['high'], df['low'], df['close'], df['volume'], fast=3, slow=10)
        if chaikin is not None and not chaikin.empty and chaikin.iloc[-1] > 0:
            signals["volume"] += 1

        # ✅ 6. OBV
        obv = ta.obv(df['close'], df['volume'])
        if obv is not None and not obv.empty and obv.iloc[-1] > obv.iloc[-15]:
            signals["volume"] += 1

        # ========================== VOLATILITY ==========================
        # ✅ 7. ATR(15)
        atr = ta.atr(df['high'], df['low'], df['close'], length=15)
        if atr is not None and not atr.empty and atr.iloc[-1] > atr.iloc[-5]:
            signals["volatility"] += 1

        # ✅ 8. Bollinger Bands(30,2)
        bbands = ta.bbands(df['close'], length=30, std=2)
        if bbands is not None and not bbands.empty and df['close'].iloc[-1] > bbands.iloc[-1]['BBL_30_2.0']:
            signals["volatility"] += 1

        # ================== SUPPORT/RESISTANCE ==========================
        # ✅ 9. Gann Fan approximation: higher highs
        if df['high'].iloc[-1] > df['high'].iloc[-2] > df['high'].iloc[-3]:
            signals["support_resistance"] += 1

        # ✅ 10. Fibonacci Retracement Support zone
        recent_close = df['close'].iloc[-1]
        high = df['high'].max()
        low = df['low'].min()
        fib_0_618 = high - 0.618 * (high - low)
        if recent_close >= fib_0_618:
            signals["support_resistance"] += 1

        symbol = df['symbol'].iloc[-1] if 'symbol' in df.columns else df.iloc[-1]['symbol']
        insert_indicator_signal(cursor, symbol, signals)
        print(f"✅ Signals stored for {symbol}")

    except Exception as e:
        print(f"❌ Indicator computation failed: {e}")
