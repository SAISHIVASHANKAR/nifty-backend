# indicators.py

import numpy as np
import pandas as pd
from utils import insert_indicator_signal

def compute_all_indicators(symbol, df, cursor):
    trend_score = 0
    momentum_score = 0
    volume_score = 0
    volatility_score = 0
    support_resistance_score = 0

    try:
        df = df.copy()

        # === Trend Indicators ===
        ## 1. ADX(15)
        df['TR'] = np.maximum(df['High'] - df['Low'],
                              np.maximum(abs(df['High'] - df['Close'].shift()),
                                         abs(df['Low'] - df['Close'].shift())))
        df['+DM'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']),
                             np.maximum(df['High'] - df['High'].shift(), 0), 0)
        df['-DM'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()),
                             np.maximum(df['Low'].shift() - df['Low'], 0), 0)
        TR14 = df['TR'].rolling(window=15).sum()
        plusDM14 = df['+DM'].rolling(window=15).sum()
        minusDM14 = df['-DM'].rolling(window=15).sum()
        plusDI14 = 100 * (plusDM14 / TR14)
        minusDI14 = 100 * (minusDM14 / TR14)
        DX = 100 * abs(plusDI14 - minusDI14) / (plusDI14 + minusDI14)
        df['ADX'] = DX.rolling(window=15).mean()
        if df['ADX'].iloc[-1] > 20:
            trend_score += 1

        ## 2. VWAP(10)
        df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (df['TP'] * df['Volume']).rolling(window=10).sum() / df['Volume'].rolling(window=10).sum()
        if df['Close'].iloc[-1] > df['VWAP'].iloc[-1]:
            trend_score += 1

        # === Momentum Indicators ===
        ## 3. MACD (18, 36, 9)
        df['EMA18'] = df['Close'].ewm(span=18, adjust=False).mean()
        df['EMA36'] = df['Close'].ewm(span=36, adjust=False).mean()
        df['MACD'] = df['EMA18'] - df['EMA36']
        df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        if df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1]:
            momentum_score += 1

        ## 4. RSI(15)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=15).mean()
        avg_loss = loss.rolling(window=15).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        if df['RSI'].iloc[-1] < 70 and df['RSI'].iloc[-1] > 30:
            momentum_score += 1

        # === Volume Indicators ===
        ## 5. Chaikin Oscillator (15)
        adl = ((2 * df['Close'] - df['High'] - df['Low']) / (df['High'] - df['Low']).replace(0, np.nan)) * df['Volume']
        adl = adl.cumsum()
        df['Chaikin'] = adl.ewm(span=3, adjust=False).mean() - adl.ewm(span=10, adjust=False).mean()
        if df['Chaikin'].iloc[-1] > 0:
            volume_score += 1

        ## 6. OBV
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        if df['OBV'].iloc[-1] > df['OBV'].iloc[-2]:
            volume_score += 1

        # === Volatility Indicators ===
        ## 7. ATR(15)
        df['H-L'] = df['High'] - df['Low']
        df['H-PC'] = abs(df['High'] - df['Close'].shift())
        df['L-PC'] = abs(df['Low'] - df['Close'].shift())
        tr = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
        df['ATR'] = tr.rolling(window=15).mean()
        if df['ATR'].iloc[-1] > df['ATR'].mean():
            volatility_score += 1

        ## 8. Bollinger Bands(30, 2 std dev)
        ma30 = df['Close'].rolling(window=30).mean()
        std30 = df['Close'].rolling(window=30).std()
        df['UpperBand'] = ma30 + 2 * std30
        df['LowerBand'] = ma30 - 2 * std30
        if df['Close'].iloc[-1] < df['UpperBand'].iloc[-1] and df['Close'].iloc[-1] > df['LowerBand'].iloc[-1]:
            volatility_score += 1

        # === Support / Resistance ===
        ## 9. Gann Fan (1:1 approximation)
        df['Gann_1_1'] = df['Close'].shift(1) + (df['Close'].diff().mean())
        if df['Close'].iloc[-1] > df['Gann_1_1'].iloc[-1]:
            support_resistance_score += 1

        ## 10. Fibonacci Retracement (swing high/low)
        swing_high = df['High'].rolling(window=30).max()
        swing_low = df['Low'].rolling(window=30).min()
        fib_0_618 = swing_high - 0.618 * (swing_high - swing_low)
        if df['Close'].iloc[-1] > fib_0_618.iloc[-1]:
            support_resistance_score += 1

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

    insert_indicator_signal(cursor, symbol, trend_score, momentum_score, volume_score, volatility_score, support_resistance_score)
