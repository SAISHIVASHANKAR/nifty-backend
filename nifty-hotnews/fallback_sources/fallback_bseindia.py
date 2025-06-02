# fallback_bseindia.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news(mode="sod"):
    print(f"[BSE] Fetching in mode: {mode}")
    
    url = "https://www.bseindia.com/markets/MarketInfo/NewsResult.aspx"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the news table
    table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvNews"})
    if not table:
        raise Exception("No news table found on BSE page.")

    rows = table.find_all("tr")[1:]  # Skip the header row

    news_items = []
    for row in rows[:10]:  # Only collect the top 10 rows
        cols = row.find_all("td")
        if len(cols) >= 2:
            time_str = cols[0].get_text(strip=True)
            headline = cols[1].get_text(strip=True)
            timestamp = f"{datetime.today().strftime('%Y-%m-%d')} {time_str}"
            news_items.append({
                "timestamp": timestamp,
                "headline": headline,
                "source": "BSE"
            })

    return {
        "source": "BSE",
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "highlights": news_items
    }

# Debug/test mode
if __name__ == "__main__":
    result = fetch_news(mode="test")
    for item in result["highlights"]:
        print(f"{item['timestamp']} ➤ {item['headline']}")
