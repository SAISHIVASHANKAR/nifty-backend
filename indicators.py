# indicators.py

import pandas_ta as ta
from utils import insert_indicator_signal

def compute_all_indicators(df, cursor, symbol):
    if df.empty or len(df) < 50:
        print(f"Not enough data to compute indicators for {symbol}")
        return

    try:
        df = df.copy()

        # Initialize signal categories
        trend = 0
        momentum = 0
        volume = 0
        volatility = 0
        support_resistance = 0

        # 1. ADX(15) - Trend
        adx = ta.adx(df['High'], df['Low'], df['Close'], length=15)
        if not adx.empty and adx['ADX_15'].iloc[-1] > 25:
            trend += 1
        elif not adx.empty and adx['ADX_15'].iloc[-1] < 20:
            trend -= 1

        # 2. VWAP(10) - Trend
        df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'], length=10)
        if df['Close'].iloc[-1] > df['VWAP'].iloc[-1]:
            trend += 1
        else:
            trend -= 1

        # 3. MACD (fast=18, slow=36, signal=9) - Momentum
        macd = ta.macd(df['Close'], fast=18, slow=36, signal=9)
        if not macd.empty and macd['MACD_18_36_9'].iloc[-1] > macd['MACDs_18_36_9'].iloc[-1]:
            momentum += 1
        else:
            momentum -= 1

        # 4. RSI(15) - Momentum
        rsi = ta.rsi(df['Close'], length=15)
        if not rsi.empty and rsi.iloc[-1] > 50:
            momentum += 1
        elif not rsi.empty and rsi.iloc[-1] < 45:
            momentum -= 1

        # 5. Chaikin Oscillator(15) - Volume
        chaikin = ta.chaikin(df['High'], df['Low'], df['Close'], df['Volume'], fast=3, slow=10)
        if not chaikin.empty and chaikin.iloc[-1] > 0:
            volume += 1
        else:
            volume -= 1

        # 6. OBV - Volume
        obv = ta.obv(df['Close'], df['Volume'])
        if not obv.empty and obv.diff().iloc[-1] > 0:
            volume += 1
        else:
            volume -= 1

        # 7. ATR(15) - Volatility
        atr = ta.atr(df['High'], df['Low'], df['Close'], length=15)
        if not atr.empty and atr.iloc[-1] > atr.iloc[-2]:
            volatility += 1
        else:
            volatility -= 1

        # 8. Bollinger Bands(30, 2) - Volatility
        bbands = ta.bbands(df['Close'], length=30, std=2)
        if not bbands.empty and df['Close'].iloc[-1] < bbands['BBL_30_2.0'].iloc[-1]:
            volatility -= 1
        elif not bbands.empty and df['Close'].iloc[-1] > bbands['BBU_30_2.0'].iloc[-1]:
            volatility += 1

        # 9. Fibonacci Retracement - Support/Resistance (static scoring)
        support_resistance += 1  # placeholder for now

        # 10. Gann Fan (1:1) - Support/Resistance (static scoring)
        support_resistance += 1  # placeholder for now

        # Log scoring
        print(f"{symbol} ⬇️ Signals: Trend={trend}, Momentum={momentum}, Volume={volume}, Volatility={volatility}, SR={support_resistance}")

        insert_indicator_signal(
            symbol,
            trend,
            momentum,
            volume,
            volatility,
            support_resistance
        )

    except Exception as e:
        print(f"Indicator computation failed for {symbol}: {e}")
