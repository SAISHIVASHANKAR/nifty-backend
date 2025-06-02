# fallback_economictimes.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    print("[Economic Times] Fetching in mode:", mode)
    return [
        {
            "timestamp": "2025-06-02 09:00:00",
            "headline": "Economic Times Top News Headline Example",
            "source": "Economic Times"
        }
    ]

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = []
        for article in soup.select(".eachStory"):
            title = article.find("h3")
            summary = article.find("p")

            if title and summary:
                news_items.append({
                    "source": "Economic Times 📊",
                    "title": title.get_text(strip=True),
                    "summary": summary.get_text(strip=True),
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": "🗣️ Expert Comments"
                })

            if len(news_items) >= 10:
                break

        return news_items

    except Exception as e:
        print(f"❌ Error fetching from ET: {e}")
        return []
