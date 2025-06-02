# fetch_and_cache_hotnews.py

import json
from fallback_sources.fallback_economictimes import fetch_news as fetch_et
from fallback_sources.fallback_bloombergquint import fetch_news as fetch_bq
from fallback_sources.fallback_moneycontrol import fetch_news as fetch_mc
from fallback_sources.fallback_business_standard import fetch_news as fetch_bs
from fallback_sources.fallback_bseindia import fetch_news as fetch_bse
def fetch_and_cache_hotnews(mode="sod"):
    all_news = []

    for source_func in [fetch_et, fetch_mc, fetch_bq, fetch_bs, fetch_bse]:
        try:
            news = source_func(mode=mode)
            if news:
                all_news.extend(news)
        except Exception as e:
            print(f"❌ Error fetching from {source_func.__name__}: {e}")

    if all_news:
        output_file = f"hotnews_cache_{mode}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_news, f, indent=2, ensure_ascii=False)
        print(f"✅ Hot news ({mode}) saved to {output_file}")
    else:
        print(f"⚠️ No news collected for mode: {mode}")

if __name__ == "__main__":
    # Automatically fetch for both SOD and EOD when run standalone
    fetch_and_cache_hotnews(mode="sod")
    fetch_and_cache_hotnews(mode="eod")
