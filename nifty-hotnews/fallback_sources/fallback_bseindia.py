# hot_news/sources/bse.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_from_bse():
    url = "https://www.bseindia.com/markets/MarketInfo/NewsResult.aspx"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Collecting news table rows
    table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvNews"})
    if not table:
        raise Exception("No news table found on BSE page.")

    rows = table.find_all("tr")[1:]  # skip header

    news_items = []
    for row in rows[:10]:  # Limit to top 10 headlines
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

# Example test
if __name__ == "__main__":
    result = fetch_from_bse()
    for item in result["highlights"]:
        print(f"{item['timestamp']} ➤ {item['headline']}")
