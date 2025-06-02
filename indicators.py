import pandas_ta as ta
import pandas as pd
from utils import insert_indicator_signal

def compute_all_indicators(df, symbol, cursor):
    if 'Date' not in df.columns:
        print(f"⚠️ Skipping {symbol}: 'Date' column missing.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    trend_score = 0
    momentum_score = 0
    volume_score = 0
    volatility_score = 0
    support_resistance_score = 0

    # Trend Indicators
    try:
        df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'], length=15)['ADX_15']
        if df['ADX'].iloc[-1] > 25:
            trend_score += 1
    except:
        print(f"Trend: ADX failed for {symbol}")

    try:
        df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
        if df['Close'].iloc[-1] > df['VWAP'].iloc[-1]:
            trend_score += 1
    except:
        print(f"Trend: VWAP failed for {symbol}")

    # Momentum Indicators
    try:
        macd = ta.macd(df['Close'], fast=18, slow=36, signal=9)
        if macd['MACD_18_36_9'].iloc[-1] > macd['MACDs_18_36_9'].iloc[-1]:
            momentum_score += 1
    except:
        print(f"Momentum: MACD failed for {symbol}")

    try:
        df['RSI'] = ta.rsi(df['Close'], length=15)
        if df['RSI'].iloc[-1] > 50:
            momentum_score += 1
    except:
        print(f"Momentum: RSI failed for {symbol}")

    # Volume Indicators
    try:
        obv = ta.obv(df['Close'], df['Volume'])
        if obv.iloc[-1] > obv.iloc[-15]:
            volume_score += 1
    except:
        print(f"Volume: OBV failed for {symbol}")

    try:
        cho = ta.ad(df['High'], df['Low'], df['Close'], df['Volume'])
        if cho.iloc[-1] > cho.iloc[-15]:
            volume_score += 1
    except:
        print(f"Volume: Chaikin failed for {symbol}")

    # Volatility Indicators
    try:
        atr = ta.atr(df['High'], df['Low'], df['Close'], length=15)
        if atr.iloc[-1] > atr.iloc[-15]:
            volatility_score += 1
    except:
        print(f"Volatility: ATR failed for {symbol}")

    try:
        bb = ta.bbands(df['Close'], length=30, std=2)
        if df['Close'].iloc[-1] < bb['BBL_30_2.0'].iloc[-1]:
            volatility_score += 1
    except:
        print(f"Volatility: BBands failed for {symbol}")

    # Support/Resistance Indicators
    try:
        df['Gann'] = df['Close'] + ((df['High'] - df['Low']) / 8)
        if df['Close'].iloc[-1] > df['Gann'].iloc[-1]:
            support_resistance_score += 1
    except:
        print(f"Support: Gann Fan failed for {symbol}")

    try:
        recent = df['Close'].tail(30)
        high = recent.max()
        low = recent.min()
        fib_0_618 = high - (high - low) * 0.618
        if df['Close'].iloc[-1] > fib_0_618:
            support_resistance_score += 1
    except:
        print(f"Support: Fibonacci failed for {symbol}")

    date = df.index[-1].strftime("%Y-%m-%d")
    insert_indicator_signal(cursor, symbol, trend_score, momentum_score, volume_score, volatility_score, support_resistance_score, date)
