# fallback_nseindia.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    url = "https://www.nseindia.com/market-data/circulars"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)  # required for cookies
        response = session.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        table_rows = soup.select("table tbody tr")

        news_items = []

        for row in table_rows[:10]:  # limit to 10
            columns = row.find_all("td")
            if len(columns) >= 2:
                title = columns[1].text.strip()
                news_items.append({
                    "source": "NSE India 📊",
                    "title": title,
                    "summary": "Market Circular or Update",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": "📊 RBI/Govt Announcements"
                })

        return news_items

    except Exception as e:
        print(f"❌ Error fetching from NSE India: {e}")
        return []
