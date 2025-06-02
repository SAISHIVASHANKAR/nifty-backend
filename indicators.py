# indicators.py

import pandas as pd
import numpy as np
import talib

def compute_all_indicators(df, cursor, symbol):
    try:
        df = df.copy()

        # Ensure 'date' column exists and is datetime
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        # RSI (15)
        df['RSI'] = talib.RSI(df['close'], timeperiod=15)
        rsi_signal = 1 if df['RSI'].iloc[-1] < 30 else -1 if df['RSI'].iloc[-1] > 70 else 0

        # MACD (fast=18, slow=36, signal=9)
        macd, signal, hist = talib.MACD(df['close'], fastperiod=18, slowperiod=36, signalperiod=9)
        macd_signal = 1 if macd.iloc[-1] > signal.iloc[-1] else -1

        # OBV
        df['OBV'] = talib.OBV(df['close'], df['volume'])
        obv_signal = 1 if df['OBV'].iloc[-1] > df['OBV'].iloc[-5] else -1

        # Bollinger Bands (30,2)
        upper, middle, lower = talib.BBANDS(df['close'], timeperiod=30, nbdevup=2, nbdevdn=2)
        bb_signal = 1 if df['close'].iloc[-1] < lower.iloc[-1] else -1 if df['close'].iloc[-1] > upper.iloc[-1] else 0

        # Fibonacci support/resistance levels (simulated)
        high = df['high'].max()
        low = df['low'].min()
        current = df['close'].iloc[-1]
        fib_signal = 1 if current < low + 0.382*(high-low) else -1 if current > high - 0.382*(high-low) else 0

        # ADX (15)
        adx = talib.ADX(df['high'], df['low'], df['close'], timeperiod=15)
        adx_signal = 1 if adx.iloc[-1] > 25 else 0

        # ATR (15)
        atr = talib.ATR(df['high'], df['low'], df['close'], timeperiod=15)
        atr_signal = 1 if atr.iloc[-1] > atr.mean() else 0

        # Chaikin Oscillator (15)
        ad = talib.AD(df['high'], df['low'], df['close'], df['volume'])
        chaikin = ad.rolling(15).mean()
        chaikin_signal = 1 if chaikin.iloc[-1] > chaikin.iloc[-2] else -1

        # Gann Fan (stub logic)
        gann_signal = 1 if current > (high + low) / 2 else -1

        # VWAP (10-day simulated)
        df['TP'] = (df['high'] + df['low'] + df['close']) / 3
        df['TPV'] = df['TP'] * df['volume']
        vwap = df['TPV'].rolling(10).sum() / df['volume'].rolling(10).sum()
        vwap_signal = 1 if df['close'].iloc[-1] > vwap.iloc[-1] else -1

        # Prepare indicator scoring
        signal_data = {
            "symbol": symbol,
            "trend": adx_signal + vwap_signal,
            "momentum": macd_signal + rsi_signal,
            "volume": chaikin_signal + obv_signal,
            "volatility": atr_signal + bb_signal,
            "support_resistance": fib_signal + gann_signal,
        }

        # Insert into DB
        cursor.execute("""
            INSERT OR REPLACE INTO indicator_signals
            (symbol, trend, momentum, volume, volatility, support_resistance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            signal_data["symbol"],
            signal_data["trend"],
            signal_data["momentum"],
            signal_data["volume"],
            signal_data["volatility"],
            signal_data["support_resistance"]
        ))

    except Exception as e:
        print(f"Error computing indicators for {symbol}: {e}")
