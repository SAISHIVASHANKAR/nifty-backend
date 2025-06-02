# fallback_businessstandard.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    print("[Business Standard] Fetching in mode:", mode)
    return [
        {
            "timestamp": "2025-06-02 09:00:00",
            "headline": "Business Standard Top News Headline Example",
            "source": "Business Standard"
        }
    ]
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = []
        articles = soup.select("div.listingPage article")

        for article in articles:
            headline = article.find("h2")
            snippet = article.find("p")

            if headline and snippet:
                news_items.append({
                    "source": "Business Standard 🏦",
                    "title": headline.get_text(strip=True),
                    "summary": snippet.get_text(strip=True),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": "🏦 FII/DII activity summaries"
                })

            if len(news_items) >= 10:
                break

        return news_items

    except Exception as e:
        print(f"❌ Error fetching from Business Standard: {e}")
        return []
