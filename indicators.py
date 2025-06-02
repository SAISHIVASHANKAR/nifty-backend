
import pandas_ta as ta
from utils import insert_indicator_signal

def compute_all_indicators(df, symbol, cursor):
    try:
        trend = 0
        momentum = 0
        volume = 0
        volatility = 0
        support_resistance = 0

        # ADX (Trend)
        if 'High' in df.columns and 'Low' in df.columns and 'Close' in df.columns:
            adx = ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=15)
            if not adx.empty and adx['ADX_15'].iloc[-1] > 25:
                trend += 1

        # VWAP (Trend)
        if 'High' in df.columns and 'Low' in df.columns and 'Close' in df.columns and 'Volume' in df.columns:
            vwap = ta.vwap(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume'])
            if not vwap.empty and df['Close'].iloc[-1] > vwap.iloc[-1]:
                trend += 1

        # MACD (Momentum)
        macd = ta.macd(close=df['Close'])
        if not macd.empty and macd['MACD_12_26_9'].iloc[-1] > macd['MACDs_12_26_9'].iloc[-1]:
            momentum += 1

        # RSI (Momentum)
        rsi = ta.rsi(close=df['Close'], length=15)
        if not rsi.empty and rsi.iloc[-1] < 70 and rsi.iloc[-1] > 50:
            momentum += 1

        # OBV (Volume)
        obv = ta.obv(close=df['Close'], volume=df['Volume'])
        if not obv.empty and obv.iloc[-1] > obv.iloc[-5]:
            volume += 1

        # Chaikin Oscillator (Volume)
        cho = ta.adosc(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume'])
        if not cho.empty and cho.iloc[-1] > 0:
            volume += 1

        # ATR (Volatility)
        atr = ta.atr(high=df['High'], low=df['Low'], close=df['Close'], length=15)
        if not atr.empty and atr.iloc[-1] > atr.iloc[-2]:
            volatility += 1

        # Bollinger Bands (Volatility)
        bb = ta.bbands(close=df['Close'], length=30, std=2)
        if not bb.empty and df['Close'].iloc[-1] < bb['BBU_30_2.0'].iloc[-1]:
            volatility += 1

        # Fibonacci (Support/Resistance)
        if len(df) >= 2 and df['Close'].iloc[-1] > df['Close'].min():
            support_resistance += 1

        # Gann Fan 1x1 (Support/Resistance)
        if df['Close'].iloc[-1] > df['Open'].iloc[-1]:
            support_resistance += 1

        insert_indicator_signal(symbol, trend, momentum, volume, volatility, support_resistance, cursor)
    except Exception as e:
        print(f"âŒcompute_all_indicators() failed for {symbol}: {e}")
