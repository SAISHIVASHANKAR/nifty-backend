import numpy as np
import pandas as pd
from utils import load_price_data, insert_indicator_signal

def compute_all_indicators(symbol, df, cursor):
    trend_score = 0
    momentum_score = 0
    volume_score = 0
    volatility_score = 0
    support_resistance_score = 0

    try:
        # ADX (Trend)
        df['14-high'] = df['High'].rolling(window=15).max()
        df['14-low'] = df['Low'].rolling(window=15).min()
        df['ATR'] = df['14-high'] - df['14-low']
        df['ADX'] = df['ATR'].rolling(window=15).mean()
        if df['ADX'].iloc[-1] > 20:
            trend_score += 1

        # VWAP (Trend)
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        if df['Close'].iloc[-1] > df['VWAP'].iloc[-1]:
            trend_score += 1

        # MACD (Momentum)
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        if df['MACD'].iloc[-1] > 0:
            momentum_score += 1

        # RSI (Momentum)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=15).mean()
        avg_loss = loss.rolling(window=15).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        if df['RSI'].iloc[-1] < 70 and df['RSI'].iloc[-1] > 30:
            momentum_score += 1

        # Chaikin Oscillator (Volume)
        adl = ((2 * df['Close'] - df['High'] - df['Low']) / (df['High'] - df['Low']) * df['Volume']).fillna(0)
        df['Chaikin'] = adl.ewm(span=3).mean() - adl.ewm(span=10).mean()
        if df['Chaikin'].iloc[-1] > 0:
            volume_score += 1

        # OBV (Volume)
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        if df['OBV'].iloc[-1] > df['OBV'].iloc[-2]:
            volume_score += 1

        # ATR (Volatility)
        df['TR'] = df['High'] - df['Low']
        df['ATR'] = df['TR'].rolling(window=15).mean()
        if df['ATR'].iloc[-1] > 0:
            volatility_score += 1

        # Bollinger Bands (Volatility)
        df['MB'] = df['Close'].rolling(30).mean()
        df['UB'] = df['MB'] + 2 * df['Close'].rolling(30).std()
        df['LB'] = df['MB'] - 2 * df['Close'].rolling(30).std()
        if df['Close'].iloc[-1] < df['UB'].iloc[-1] and df['Close'].iloc[-1] > df['LB'].iloc[-1]:
            volatility_score += 1

        # Gann Fan (Support/Resistance)
        if df['Close'].iloc[-1] > df['Close'].iloc[-2]:
            support_resistance_score += 1

        # Fibonacci Retracement (Support/Resistance)
        max_price = df['Close'].max()
        min_price = df['Close'].min()
        fib_618 = max_price - 0.618 * (max_price - min_price)
        if df['Close'].iloc[-1] > fib_618:
            support_resistance_score += 1

    except Exception as e:
        print(f"⚠️ Error computing indicators for {symbol}: {e}")

    total_score = trend + momentum + volume + volatility + support_resistance
    insert_indicator_signal(conn, symbol, trend, momentum, volume, volatility, support_resistance, count)
