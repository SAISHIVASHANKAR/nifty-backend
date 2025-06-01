import yfinance as yf
import pandas as pd

def fetch_yf(symbol, years=8):
    try:
        period = f"{years}y"
        print(f"📦 Fetching {symbol} for {period}")
        ticker = yf.Ticker(symbol + ".NS")
        df = ticker.history(period=period)
        if df.empty:
            print(f"⚠️ Yahoo returned empty DataFrame for {symbol}")
            return pd.DataFrame()
        df = df.reset_index()[["Date", "Close", "High", "Low", "Open", "Volume"]]
        df = df.dropna()
        return df
    except Exception as e:
        print(f"❌ Error fetching {symbol} for {period}: {e}")
        return pd.DataFrame()
