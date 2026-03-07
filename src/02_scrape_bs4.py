"""
02_scrape_bs4.py
----------------
Scrapes Polish food reviews from degustujemy.pl using BeautifulSoup.
Collects title, date, category and review text from 8 categories.
Saves results to data/raw/degustujemy_scraped.csv.
Note: demonstrates handling of non-ASCII (Polish) characters.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

CATEGORIES = [
    "https://degustujemy.pl/slodycze/",
    "https://degustujemy.pl/napoje/",
    "https://degustujemy.pl/przekaski/",
    "https://degustujemy.pl/nabial/",
    "https://degustujemy.pl/dania-gotowe/",
    "https://degustujemy.pl/mrozonki/",
    "https://degustujemy.pl/dodatki-do-zywnosci/",
    "https://degustujemy.pl/artykuly/",
]

results = []

for category_url in CATEGORIES:
    page = 1
    while True:
        url = f"{category_url}page/{page}/" if page > 1 else category_url
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"  Stopped at page {page} (status {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article")
        print(f"Category: {category_url.split('/')[-2]} | Page {page}: found {len(articles)} articles")

        if not articles:
            break

        for article in articles:
            link = article.select_one("a")
            date = article.select_one("time.entry-date")

            if link and link.get("href"):
                art_response = requests.get(link["href"], headers={"User-Agent": "Mozilla/5.0"})
                art_response.encoding = "utf-8"
                art_soup = BeautifulSoup(art_response.text, "html.parser")
                content = art_soup.select_one("div.entry-content")
                full_title = art_soup.select_one("h1.entry-title")
            else:
                content = None
                full_title = None

            results.append({
                "title": full_title.text.strip() if full_title else None,
                "date": date["datetime"] if date else None,
                "category": category_url.split("/")[-2],
                "review_text": content.text.strip()[:500] if content else None,
                "url": link["href"] if link else None
            })

            time.sleep(0.3)

        page += 1

df_scraped = pd.DataFrame(results)
print(f"\nTotal reviews scraped: {len(df_scraped)}")
print(f"\nEmpty values:\n{df_scraped.isnull().sum()}")
print(f"\nSample review_text:\n{df_scraped['review_text'].iloc[0]}")

os.makedirs("data/raw", exist_ok=True)
df_scraped.to_csv("data/raw/degustujemy_scraped.csv", index=False, encoding="utf-8")
print("Saved to data/raw/degustujemy_scraped.csv")
