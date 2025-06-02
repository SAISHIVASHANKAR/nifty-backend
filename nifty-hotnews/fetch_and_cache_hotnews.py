import os
import json
import logging
from datetime import datetime

# Fallback imports
from fallback_sources.fallback_moneycontrol import get_moneycontrol_news
from fallback_sources.fallback_economictimes import get_economictimes_news
from fallback_sources.fallback_business_standard import get_business_standard_news
from fallback_sources.fallback_bloombergquint import get_bloombergquint_news
from fallback_sources.fallback_bseindia import get_bse_news

# Setup logging
LOG_FILE = "logs/hotnews.log"
CACHE_FILE = "static/news_cache.json"

os.makedirs("logs", exist_ok=True)
os.makedirs("static", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_with_fallback():
    sources = [
        ("Moneycontrol", get_moneycontrol_news),
        ("Economic Times", get_economictimes_news),
        ("Business Standard", get_business_standard_news),
        ("Bloomberg Quint", get_bloombergquint_news),
        ("BSE India", get_bse_news)
    ]

    for name, fetch_func in sources:
        try:
            news_items = fetch_func()
            if news_items:
                logging.info(f"✅ News fetched from {name}")
                return {
                    "source": name,
                    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "news": news_items
                }
            else:
                logging.warning(f"⚠️ {name} returned empty list")
        except Exception as e:
            logging.error(f"❌ Error from {name}: {e}")
    
    logging.critical("🔥 All fallback sources failed")
    return {
        "source": None,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "news": []
    }

def save_cache(data):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info("✅ News cache saved")
    except Exception as e:
        logging.error(f"❌ Failed to save cache: {e}")

if __name__ == "__main__":
    result = fetch_with_fallback()
    save_cache(result)
