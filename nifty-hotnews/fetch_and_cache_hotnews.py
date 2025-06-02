# fetch_and_cache_hotnews.py
import os
from datetime import datetime
from fallback_sources import fallback_moneycontrol, fallback_economictimes, fallback_livemint, fallback_businessline, fallback_investing

MODE = "sod" if datetime.now().hour < 12 else "eod"
OUTPUT_PATH = f"static/hotnews_{MODE}.json"

def fetch_news():
    for source_func in [
        fallback_moneycontrol.fetch_news,
        fallback_economictimes.fetch_news,
        fallback_livemint.fetch_news,
        fallback_businessline.fetch_news,
        fallback_investing.fetch_news,
    ]:
        try:
            print(f"Trying {source_func.__name__} ...")
            news = source_func(MODE)
            if news and isinstance(news, list):
                print(f"✅ Fetched from {source_func.__name__}")
                return news
        except Exception as e:
            print(f"❌ {source_func.__name__} failed: {e}")
    return []

def save_to_json(news):
    import json
    with open(OUTPUT_PATH, "w") as f:
        json.dump(news, f, indent=2, ensure_ascii=False)
    print(f"📦 Saved {len(news)} articles to {OUTPUT_PATH}")

if __name__ == "__main__":
    headlines = fetch_news()
    if headlines:
        save_to_json(headlines)
    else:
        print("⚠️ No news could be fetched.")
