import pandas as pd
import pandas_ta as ta
from utils import insert_into_indicator_signals

def compute_all_indicators(df, symbol, cursor):
    try:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])     # Ensure datetime format
        df.set_index('date', inplace=True)          # Set date as index
        df.index = df.index.tz_localize(None)       # Remove timezone to avoid warnings
        score = {
            "trend": 0,
            "momentum": 0,
            "volume": 0,
            "volatility": 0,
            "support_resistance": 0
        }

        # Trend
        adx = ta.adx(df['high'], df['low'], df['close'], length=15)
        vwap = ta.vwap(df['high'], df['low'], df['close'], df['volume'], length=10)
        if not adx.empty and adx['ADX_15'].iloc[-1] > 25:
            score['trend'] += 1
        if not vwap.empty and df['close'].iloc[-1] > vwap.iloc[-1]:
            score['trend'] += 1

        # Momentum
        macd = ta.macd(df['close'], fast=18, slow=36, signal=9)
        rsi = ta.rsi(df['close'], length=15)
        if not macd.empty and macd['MACD_18_36_9'].iloc[-1] > macd['MACDs_18_36_9'].iloc[-1]:
            score['momentum'] += 1
        if not rsi.empty and rsi.iloc[-1] > 50:
            score['momentum'] += 1

        # Volume
        obv = ta.obv(df['close'], df['volume'])
        cho = ta.ad(df['high'], df['low'], df['close'], df['volume'])
        if not obv.empty and obv.iloc[-1] > obv.iloc[-2]:
            score['volume'] += 1
        if not cho.empty and cho.iloc[-1] > cho.iloc[-2]:
            score['volume'] += 1

        # Volatility
        atr = ta.atr(df['high'], df['low'], df['close'], length=15)
        bb = ta.bbands(df['close'], length=30, std=2)
        if not atr.empty and atr.iloc[-1] > atr.iloc[-2]:
            score['volatility'] += 1
        if not bb.empty and df['close'].iloc[-1] > bb['BBM_30_2.0'].iloc[-1]:
            score['volatility'] += 1

        # Support/Resistance
        fib_high = df['high'].rolling(window=30).max().iloc[-1]
        fib_low = df['low'].rolling(window=30).min().iloc[-1]
        current = df['close'].iloc[-1]
        levels = [
            fib_high,
            fib_low,
            fib_low + 0.236 * (fib_high - fib_low),
            fib_low + 0.382 * (fib_high - fib_low),
            fib_low + 0.618 * (fib_high - fib_low)
        ]
        if any(abs(current - lvl) / current < 0.01 for lvl in levels):
            score['support_resistance'] += 1

        insert_into_indicator_signals(cursor, symbol,
                                      score['trend'], score['momentum'],
                                      score['volume'], score['volatility'],
                                      score['support_resistance'])

        return (score['trend'], score['momentum'], score['volume'],
                score['volatility'], score['support_resistance'])

    except Exception as e:
        print(f"❌ Error in compute_all_indicators() for {symbol}: {e}")
        return (0, 0, 0, 0, 0)
