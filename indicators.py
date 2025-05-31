import pandas as pd
import numpy as np

def compute_adx(df, period=15):
    df['TR'] = np.maximum(df['High'] - df['Low'],
                  np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
    df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),
                         np.maximum((df['High'] - df['High'].shift(1)), 0), 0)
    df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)),
                         np.maximum((df['Low'].shift(1) - df['Low']), 0), 0)
    TR14 = df['TR'].rolling(window=period).sum()
    plus_DM14 = df['+DM'].rolling(window=period).sum()
    minus_DM14 = df['-DM'].rolling(window=period).sum()
    plus_DI14 = 100 * (plus_DM14 / TR14)
    minus_DI14 = 100 * (minus_DM14 / TR14)
    dx = 100 * (abs(plus_DI14 - minus_DI14) / (plus_DI14 + minus_DI14))
    adx = dx.rolling(window=period).mean()
    return adx

def compute_rsi(df, period=15):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(df, fast=5, slow=20, signal=60):
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd - signal_line

def compute_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'][i] > df['Close'][i-1]:
            obv.append(obv[-1] + df['Volume'][i])
        elif df['Close'][i] < df['Close'][i-1]:
            obv.append(obv[-1] - df['Volume'][i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)

def compute_chaikin(df, period=15):
    mfm = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low']).replace(0, np.nan)
    mfv = mfm * df['Volume']
    adl = mfv.cumsum()
    ema3 = adl.ewm(span=3, adjust=False).mean()
    ema10 = adl.ewm(span=10, adjust=False).mean()
    return ema3 - ema10

def compute_atr(df, period=15):
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift(1))
    low_close = abs(df['Low'] - df['Close'].shift(1))
    tr = high_low.combine(high_close, max).combine(low_close, max)
    return tr.rolling(window=period).mean()

def compute_bollinger(df, period=30):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    return upper_band, lower_band

def compute_fibonacci_support_resistance(df):
    max_price = df['High'].max()
    min_price = df['Low'].min()
    diff = max_price - min_price
    levels = {
        '0.0%': max_price,
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50.0%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100.0%': min_price
    }
    return levels

def compute_gann_fan(df):
    df['gann'] = df['Close'].shift(1) + (df['Close'].shift(1) * 0.125)
    return df['gann']

def compute_vwap(df, period=10):
    pv = df['Close'] * df['Volume']
    rolling_pv = pv.rolling(window=period).sum()
    rolling_vol = df['Volume'].rolling(window=period).sum()
    return rolling_pv / rolling_vol

def compute_all_indicators(df):
    results = {}

    adx = compute_adx(df)
    rsi = compute_rsi(df)
    macd = compute_macd(df)
    obv = compute_obv(df)
    chaikin = compute_chaikin(df)
    atr = compute_atr(df)
    upper, lower = compute_bollinger(df)
    fib = compute_fibonacci_support_resistance(df)
    gann = compute_gann_fan(df)
    vwap = compute_vwap(df)

    results['trend'] = sum([
        adx.iloc[-1] > 25,
        vwap.iloc[-1] < df['Close'].iloc[-1]
    ])

    results['momentum'] = sum([
        rsi.iloc[-1] > 50,
        macd.iloc[-1] > 0
    ])

    results['volume'] = sum([
        obv.iloc[-1] > obv.mean(),
        chaikin.iloc[-1] > 0
    ])

    results['volatility'] = sum([
        atr.iloc[-1] > atr.mean(),
        df['Close'].iloc[-1] > upper.iloc[-1] or df['Close'].iloc[-1] < lower.iloc[-1]
    ])

    results['support_resistance'] = sum([
        df['Close'].iloc[-1] > fib['61.8%'],
        df['Close'].iloc[-1] > gann.iloc[-1]
    ])

    return results
