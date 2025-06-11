# ~/Documents/Amazon/nifty-backend/indicators.py
from utils import get_db_connection, get_all_symbols, get_cached_df, insert_into_indicator_signals
import pandas_ta as ta

def compute_all_indicators(df):
    result = {
        'trend': 0,
        'momentum': 0,
        'volume': 0,
        'volatility': 0,
        'support_resistance': 0
    }

    try:
        df.ta.adx(length=15, append=True)
        adx_value = df['ADX_15'].iloc[-1]
        if adx_value > 25:
            result['trend'] += 1
    except:
        pass

    try:
        df.ta.vwap(append=True)
        if df['close'].iloc[-1] > df['VWAP_D'].iloc[-1]:
            result['trend'] += 1
    except:
        pass

    try:
        macd = ta.macd(df['close'])
        if macd['MACDh_12_26_9'].iloc[-1] > 0:
            result['momentum'] += 1
    except:
        pass

    try:
        rsi = ta.rsi(df['close'], length=15)
        if rsi.iloc[-1] > 50:
            result['momentum'] += 1
    except:
        pass

    try:
        df['OBV'] = ta.obv(df['close'], df['volume'])
        if df['OBV'].iloc[-1] > df['OBV'].iloc[-5]:
            result['volume'] += 1
    except:
        pass

    try:
        chaikin = ta.adosc(df['high'], df['low'], df['close'], df['volume'], fast=3, slow=10)
        if chaikin.iloc[-1] > 0:
            result['volume'] += 1
    except:
        pass

    try:
        atr = ta.atr(df['high'], df['low'], df['close'], length=15)
        if atr.iloc[-1] > atr.mean():
            result['volatility'] += 1
    except:
        pass

    try:
        bb = ta.bbands(df['close'], length=30, std=2)
        if df['close'].iloc[-1] < bb['BBL_30_2.0'].iloc[-1] or df['close'].iloc[-1] > bb['BBU_30_2.0'].iloc[-1]:
            result['volatility'] += 1
    except:
        pass

    try:
        close = df['close']
        max_high = df['high'].rolling(window=10).max()
        min_low = df['low'].rolling(window=10).min()
        if close.iloc[-1] <= min_low.iloc[-1] or close.iloc[-1] >= max_high.iloc[-1]:
            result['support_resistance'] += 1
    except:
        pass

    return result

def process_indicators():
    conn = get_db_connection()
    cursor = conn.cursor()
    symbols = get_all_symbols(cursor)

    for symbol in symbols:
        df = get_cached_df(symbol)
        if df.empty or len(df) < 30:
            continue

        signals = compute_all_indicators(df)
        insert_into_indicator_signals(
            cursor,
            symbol,
            signals['trend'],
            signals['momentum'],
            signals['volume'],
            signals['volatility'],
            signals['support_resistance']
        )

    conn.commit()
    conn.close()
