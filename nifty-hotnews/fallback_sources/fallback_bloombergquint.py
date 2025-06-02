# fallback_bloombergquint.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    url = "https://www.bqprime.com/markets"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("article")[:10]  # Limit to top 10
        news_items = []

        for art in articles:
            title_tag = art.find("h3")
            summary_tag = art.find("p")

            title = title_tag.text.strip() if title_tag else "No Title"
            summary = summary_tag.text.strip() if summary_tag else "No Summary"

            news_items.append({
                "source": "BQ Prime 🗣️",
                "title": title,
                "summary": summary,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": "🗣️ Expert Comments"
            })

        return news_items

    except Exception as e:
        print(f"❌ Error fetching from BQ Prime: {e}")
        return []
