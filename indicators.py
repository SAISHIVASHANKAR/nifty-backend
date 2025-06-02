import pandas_ta as ta
import pandas as pd
from utils import insert_signal  # ✅ Corrected import
import traceback

def compute_all_indicators(df, symbol, cursor):
    try:
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        df.sort_index(inplace=True)

        trend = 0
        momentum = 0
        volume = 0
        volatility = 0
        support_resistance = 0

        # Trend: ADX(15)
        try:
            adx = ta.adx(df["High"], df["Low"], df["Close"], length=15)
            if adx["ADX_15"].iloc[-1] > 25:
                trend += 1
        except:
            pass

        # Trend: VWAP(10)
        try:
            df["VWAP"] = ta.vwap(df["High"], df["Low"], df["Close"], df["Volume"], anchor="M")
            if df["Close"].iloc[-1] > df["VWAP"].iloc[-1]:
                trend += 1
        except:
            pass

        # Momentum: MACD
        try:
            macd = ta.macd(df["Close"])
            if macd["MACD_12_26_9"].iloc[-1] > macd["MACDs_12_26_9"].iloc[-1]:
                momentum += 1
        except:
            pass

        # Momentum: RSI(15)
        try:
            rsi = ta.rsi(df["Close"], length=15)
            if rsi.iloc[-1] > 50:
                momentum += 1
        except:
            pass

        # Volume: OBV
        try:
            obv = ta.obv(df["Close"], df["Volume"])
            if obv.iloc[-1] > obv.iloc[-5]:
                volume += 1
        except:
            pass

        # Volume: Chaikin Oscillator(15)
        try:
            chaikin = ta.chaikin(df["High"], df["Low"], df["Close"], df["Volume"], short=3, long=10)
            if chaikin.iloc[-1] > 0:
                volume += 1
        except:
            pass

        # Volatility: ATR(15)
        try:
            atr = ta.atr(df["High"], df["Low"], df["Close"], length=15)
            if atr.iloc[-1] > atr.iloc[-5]:
                volatility += 1
        except:
            pass

        # Volatility: Bollinger Bands(30)
        try:
            bbands = ta.bbands(df["Close"], length=30, std=2)
            if df["Close"].iloc[-1] > bbands["BBL_30_2.0"].iloc[-1]:
                volatility += 1
        except:
            pass

        # Support/Resistance: Fibonacci retracement (assumed: high/low comparison)
        try:
            recent_high = df["High"].iloc[-30:].max()
            recent_low = df["Low"].iloc[-30:].min()
            current = df["Close"].iloc[-1]
            fib_support = recent_low + 0.618 * (recent_high - recent_low)
            if current > fib_support:
                support_resistance += 1
        except:
            pass

        # Support/Resistance: Gann Fan (simplified slope-based)
        try:
            slope = (df["Close"].iloc[-1] - df["Close"].iloc[-30]) / 30
            if slope > 0:
                support_resistance += 1
        except:
            pass

        # Save signals
        insert_signal(symbol, trend, momentum, volume, volatility, support_resistance, cursor)

    except Exception as e:
        print(f"❌compute_all_indicators() failed for {symbol}: {str(e)}")
        traceback.print_exc()
