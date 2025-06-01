# fallback_bse.py

import requests
import pandas as pd
from utils import insert_into_prices_table
from datetime import datetime
import io

def fetch_bse(symbol):
    print(f"📦 Trying BSE for {symbol}")

    try:
        # This is just placeholder logic — BSE doesn't offer reliable EOD download by symbol
        print(f"❌ BSE fallback not implemented: {symbol}")
        return False

    except Exception as e:
        print(f"❌ BSE fallback error for {symbol}: {e}")
        return False
