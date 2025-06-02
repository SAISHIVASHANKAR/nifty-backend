# indicators.py

import pandas_ta as ta

def compute_all_indicators(df):
    df = df.copy()
    
    # ADX(15)
    df['ADX'] = ta.adx(df['high'], df['low'], df['close'], length=15)['ADX_15']

    # VWAP(10)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])

    # MACD(18, 36, 9)
    macd = ta.macd(df['close'], fast=18, slow=36, signal=9)
    df['MACD'] = macd['MACD_18_36_9']
    df['MACD_signal'] = macd['MACDs_18_36_9']

    # RSI(15)
    df['RSI'] = ta.rsi(df['close'], length=15)

    # Chaikin Oscillator(15)
    chaikin = ta.chaikin(df['high'], df['low'], df['close'], df['volume'], fast=3, slow=10)
    df['Chaikin'] = chaikin

    # OBV
    df['OBV'] = ta.obv(df['close'], df['volume'])

    # ATR(15)
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=15)

    # Bollinger Bands(30, 2)
    bb = ta.bbands(df['close'], length=30, std=2)
    df['BB_upper'] = bb['BBU_30_2.0']
    df['BB_lower'] = bb['BBL_30_2.0']

    # Fibonacci Retracement not needed to be added in column, used for S/R scoring only
    # Gann Fan (1:1) placeholder logic: using trendline direction
    df['GANN'] = df['close'].diff(7)

    return df

def generate_scores(df):
    scores = {
        "trend": 0,
        "momentum": 0,
        "volume": 0,
        "volatility": 0,
        "support_resistance": 0
    }

    if df.empty or len(df) < 30:
        return scores

    latest = df.iloc[-1]

    # Trend: ADX + VWAP
    if latest['ADX'] > 25:
        scores["trend"] += 1
    if latest['close'] > latest['VWAP']:
        scores["trend"] += 1
    else:
        scores["trend"] -= 1

    # Momentum: MACD + RSI
    if latest['MACD'] > latest['MACD_signal']:
        scores["momentum"] += 1
    else:
        scores["momentum"] -= 1
    if latest['RSI'] > 55:
        scores["momentum"] += 1
    elif latest['RSI'] < 45:
        scores["momentum"] -= 1

    # Volume: OBV + Chaikin
    if latest['Chaikin'] > 0:
        scores["volume"] += 1
    else:
        scores["volume"] -= 1
    if df['OBV'].iloc[-1] > df['OBV'].iloc[-5]:
        scores["volume"] += 1
    else:
        scores["volume"] -= 1

    # Volatility: ATR + Bollinger Bands
    if latest['ATR'] > df['ATR'].mean():
        scores["volatility"] += 1
    if latest['close'] < latest['BB_lower']:
        scores["volatility"] -= 1
    elif latest['close'] > latest['BB_upper']:
        scores["volatility"] += 1

    # Support/Resistance: Fibonacci + GANN
    if df['close'].iloc[-1] > df['close'].max() * 0.786:
        scores["support_resistance"] -= 1
    elif df['close'].iloc[-1] < df['close'].min() * 1.236:
        scores["support_resistance"] += 1

    if latest['GANN'] > 0:
        scores["support_resistance"] += 1

    return scores
