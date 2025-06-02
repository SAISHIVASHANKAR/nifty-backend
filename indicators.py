# indicators.py

import pandas as pd
import pandas_ta as ta
from utils import insert_indicator_signal

def compute_all_indicators(df, symbol, cursor):
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_cols):
        missing = set(required_cols) - set(df.columns)
        print(f"⚠️ Skipping {symbol}: missing columns {missing}")
        return

    try:
        df['ADX'] = ta.adx(df['high'], df['low'], df['close'], length=15).iloc[:, 0]
        df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
        df['MACD'] = ta.macd(df['close'], fast=18, slow=36, signal=9).iloc[:, 0]
        df['RSI'] = ta.rsi(df['close'], length=15)
        df['OBV'] = ta.obv(df['close'], df['volume'])
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=15)
        df['BOLL'] = ta.bbands(df['close'], length=30, std=2)['BBM_30_2.0']
        df['CHA'] = ta.chaikin(df['high'], df['low'], df['close'], df['volume'])
        df['FIB'] = (df['close'] - df['low'].rolling(14).min()) / (df['high'].rolling(14).max() - df['low'].rolling(14).min())
        df['GANN'] = (df['high'] + df['low']) / 2

        # Defensive scoring
        trend = int(df['ADX'].iloc[-1] > 25 if not df['ADX'].isna().all() else 0) + \
                int(df['VWAP'].iloc[-1] > df['close'].iloc[-1] if not df['VWAP'].isna().all() else 0)

        momentum = int(df['MACD'].iloc[-1] > 0 if not df['MACD'].isna().all() else 0) + \
                   int(df['RSI'].iloc[-1] > 50 if not df['RSI'].isna().all() else 0)

        volume = int(df['OBV'].iloc[-1] > df['OBV'].iloc[-15] if len(df['OBV'].dropna()) >= 16 else 0) + \
                 int(df['CHA'].iloc[-1] > 0 if not df['CHA'].isna().all() else 0)

        volatility = int(df['ATR'].iloc[-1] > df['ATR'].mean() if not df['ATR'].isna().all() else 0) + \
                     int(df['BOLL'].iloc[-1] > df['close'].iloc[-1] if not df['BOLL'].isna().all() else 0)

        support_resistance = int(df['FIB'].iloc[-1] < 0.382 if not df['FIB'].isna().all() else 0) + \
                             int(df['GANN'].iloc[-1] < df['close'].iloc[-1] if not df['GANN'].isna().all() else 0)

        insert_indicator_signal(cursor, symbol, {
            "trend": trend,
            "momentum": momentum,
            "volume": volume,
            "volatility": volatility,
            "support_resistance": support_resistance
        })

    except Exception as e:
        print(f"❌ Indicator computation failed for {symbol}: {e}")
