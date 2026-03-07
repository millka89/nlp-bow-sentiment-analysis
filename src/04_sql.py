"""
04_sql.py
---------
Loads scraped and downloaded data into SQLite database.
Performs exploratory SQL queries on both data sources:
- amazon_reviews: 568k Amazon food reviews (Kaggle)
- polish_reviews: 213 Polish food reviews (degustujemy.pl)
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "data/processed/reviews.db"
os.makedirs("data/processed", exist_ok=True)

#Load CSV 
print("Loading CSV files...")
df_kaggle = pd.read_csv("data/Reviews.csv")
df_polish = pd.read_csv("data/raw/degustujemy_translated.csv", encoding="utf-8")
# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
print(f"Connected to database: {DB_PATH}")

# Save to SQL tables
df_kaggle.to_sql("amazon_reviews", conn, if_exists="replace", index=False)
print(f"Table 'amazon_reviews' created: {len(df_kaggle)} rows")

df_polish.to_sql("polish_reviews", conn, if_exists="replace", index=False)
print(f"Table 'polish_reviews' created: {len(df_polish)} rows")

# Query 1 — score distribution
print("\n--- Score distribution (Amazon) ---")
query1="""
SELECT Score, COUNT(*) as count
FROM amazon_reviews
GROUP BY Score
ORDER BY Score
"""
print(pd.read_sql(query1, conn))

# Query 2 — average score per year
print("\n--- Average score per year (Amazon) ---")
query2 = """
    SELECT 
        strftime('%Y', datetime(Time, 'unixepoch')) AS year,
        ROUND(AVG(Score), 2) AS avg_score,
        COUNT(*) AS total_reviews
    FROM amazon_reviews
    GROUP BY year
    ORDER BY year
"""
print(pd.read_sql(query2, conn))

# Query 3 — category distribution (Polish)
print("\n--- Category distribution (Polish reviews) ---")
query3 = """
    SELECT category, COUNT(*) as count
    FROM polish_reviews
    GROUP BY category
    ORDER BY count DESC
"""
print(pd.read_sql(query3, conn))

# Query 4 — most reviewed products (Amazon)
print("\n--- Top 10 most reviewed products (Amazon) ---")
query4 = """
    SELECT ProductId, COUNT(*) as review_count
    FROM amazon_reviews
    GROUP BY ProductId
    ORDER BY review_count DESC
    LIMIT 10
"""
print(pd.read_sql(query4, conn))

conn.close()
print("\nDatabase connection closed.")
print(f"Database saved to: {DB_PATH}")