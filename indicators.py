import pandas as pd
import numpy as np

# ADX (Average Directional Index) for trend
def get_adx_signal(df, period=15):
    df['TR'] = np.maximum(df['High'] - df['Low'],
                 np.maximum(abs(df['High'] - df['Close'].shift()), abs(df['Low'] - df['Close'].shift())))
    df['+DM'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']), 
                         np.maximum(df['High'] - df['High'].shift(), 0), 0)
    df['-DM'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()), 
                         np.maximum(df['Low'].shift() - df['Low'], 0), 0)
    
    tr_smooth = df['TR'].rolling(window=period).sum()
    plus_di = 100 * (df['+DM'].rolling(window=period).sum() / tr_smooth)
    minus_di = 100 * (df['-DM'].rolling(window=period).sum() / tr_smooth)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()

    if adx.iloc[-1] > 25:
        return "Buy"
    elif adx.iloc[-1] < 20:
        return "Sell"
    else:
        return "Hold"

# Stochastic Oscillator for momentum
def get_stochastic_signal(df, period=15):
    low_min = df['Low'].rolling(window=period).min()
    high_max = df['High'].rolling(window=period).max()
    k = 100 * (df['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(3).mean()

    if k.iloc[-1] > 80 and d.iloc[-1] > 80:
        return "Sell"
    elif k.iloc[-1] < 20 and d.iloc[-1] < 20:
        return "Buy"
    else:
        return "Hold"

# Chaikin Oscillator for volume
def get_chaikin_signal(df, period=15):
    mfv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low']) * df['Volume']
    adl = mfv.cumsum()
    ema3 = adl.ewm(span=3, adjust=False).mean()
    ema10 = adl.ewm(span=10, adjust=False).mean()
    chaikin = ema3 - ema10

    if chaikin.iloc[-1] > 0:
        return "Buy"
    elif chaikin.iloc[-1] < 0:
        return "Sell"
    else:
        return "Hold"

# ATR (Average True Range) for volatility
def get_atr_signal(df, period=15):
    tr = df[['High', 'Low', 'Close']].copy()
    tr['h-l'] = df['High'] - df['Low']
    tr['h-c'] = abs(df['High'] - df['Close'].shift())
    tr['l-c'] = abs(df['Low'] - df['Close'].shift())
    tr['TR'] = tr[['h-l', 'h-c', 'l-c']].max(axis=1)
    atr = tr['TR'].rolling(window=period).mean()

    change = df['Close'].pct_change()
    if change.iloc[-1] > (atr.iloc[-1] / df['Close'].iloc[-1]):
        return "Buy"
    elif change.iloc[-1] < -(atr.iloc[-1] / df['Close'].iloc[-1]):
        return "Sell"
    else:
        return "Hold"

# Gann Fan (1:1 line logic) for support/resistance
def get_gann_fan_signal(df):
    recent_high = df['High'].rolling(window=15).max()
    recent_low = df['Low'].rolling(window=15).min()
    last_close = df['Close'].iloc[-1]
    support = recent_low.iloc[-1] + ((recent_high.iloc[-1] - recent_low.iloc[-1]) / 2)

    if last_close < support:
        return "Support"
    elif last_close > support:
        return "Resistance"
    else:
        return "Neutral"

# MACD (Momentum)
def get_macd_signal(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    if macd.iloc[-1] > signal.iloc[-1]:
        return "Buy"
    elif macd.iloc[-1] < signal.iloc[-1]:
        return "Sell"
    else:
        return "Hold"

# RSI (Momentum)
def get_rsi_signal(df, period=15):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if rsi.iloc[-1] > 70:
        return "Sell"
    elif rsi.iloc[-1] < 30:
        return "Buy"
    else:
        return "Hold"

# OBV (On-Balance Volume) (Volume)
def get_obv_signal(df):
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    if obv[-1] > obv[-2]:
        return "Buy"
    elif obv[-1] < obv[-2]:
        return "Sell"
    else:
        return "Hold"

# Bollinger Bands (Volatility)
def get_bollinger_signal(df, period=30):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)

    if df['Close'].iloc[-1] > upper.iloc[-1]:
        return "Sell"
    elif df['Close'].iloc[-1] < lower.iloc[-1]:
        return "Buy"
    else:
        return "Hold"

# Fibonacci Retracement (Support/Resistance)
def get_fibonacci_signal(df):
    max_price = df['High'].rolling(window=30).max().iloc[-1]
    min_price = df['Low'].rolling(window=30).min().iloc[-1]
    diff = max_price - min_price
    levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    close = df['Close'].iloc[-1]

    for level in levels:
        retracement = max_price - (diff * level)
        if abs(close - retracement) / close < 0.005:
            return "Resistance" if close > retracement else "Support"
    return "Neutral"

# Aggregated logic (Final output)
def compute_all_indicators(df):
    return {
        "trend": get_adx_signal(df),
        "momentum": get_stochastic_signal(df),
        "volume": get_chaikin_signal(df),
        "volatility": get_atr_signal(df),
        "support_resistance": get_gann_fan_signal(df)
  }
