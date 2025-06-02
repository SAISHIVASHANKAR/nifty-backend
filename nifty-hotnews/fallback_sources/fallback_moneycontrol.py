# fallback_moneycontrol.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    print("[Moneycontrol] Fetching in mode:", mode)
    return [
        {
            "timestamp": "2025-06-02 09:00:00",
            "headline": "Moneycontrol Top News Headline Example",
            "source": "Moneycontrol"
        }
    ]
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select(".clearfix .g_14bl"):
        title_tag = item.find("a")
        summary_tag = item.find_next("p")

        if title_tag and summary_tag:
            articles.append({
                "source": "Moneycontrol 🗣️",
                "title": title_tag.text.strip(),
                "summary": summary_tag.text.strip(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": "📈 Market Movers"
            })

        if len(articles) >= 10:
            break

    return articles
