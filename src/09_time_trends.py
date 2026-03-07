"""
09_time_trends.py
Word trends over time + rating trends.
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# --- Load data with timestamps ---
print("Loading data...")
conn = sqlite3.connect("data/processed/reviews.db")
df = pd.read_sql("""
    SELECT Time, Score, Text 
    FROM amazon_reviews 
    WHERE Text IS NOT NULL
""", conn)
conn.close()

df['year'] = pd.to_datetime(df['Time'], unit='s').dt.year
df = df[df['year'].between(2005, 2012)]  # pełne lata z wystarczającą ilością danych

# --- Rating trend over time ---
rating_trend = df.groupby('year')['Score'].mean().reset_index()

plt.figure(figsize=(10, 4))
plt.plot(rating_trend['year'], rating_trend['Score'], marker='o', color='steelblue')
plt.title('Average Rating Over Time')
plt.xlabel('Year')
plt.ylabel('Average Score')
plt.ylim(1, 5)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/processed/rating_trend.png', dpi=150)
plt.close()
print("Saved: rating_trend.png")

# --- Word trends for selected keywords ---
keywords = ['delici', 'horribl', 'organic', 'love', 'worst', 'fresh']

def word_freq_per_year(df, word):
    return df[df['Text'].str.lower().str.contains(word, na=False)].groupby('year').size()

total_per_year = df.groupby('year').size()

plt.figure(figsize=(12, 6))
for word in keywords:
    freq = word_freq_per_year(df, word) / total_per_year * 100
    plt.plot(freq.index, freq.values, marker='o', label=word)

plt.title('Word Frequency Trends Over Time (% of reviews)')
plt.xlabel('Year')
plt.ylabel('% of reviews containing word')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/processed/word_trends.png', dpi=150)
plt.close()
print("Saved: word_trends.png")

print("\nRating trend:")
print(rating_trend)
