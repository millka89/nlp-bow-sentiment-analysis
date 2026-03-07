"""
10_export_for_powerbi.py
Export all data needed for Power BI dashboard.
"""

import pandas as pd
import sqlite3
from collections import Counter
from nltk.util import ngrams

print("Loading data...")

# --- 1. Preprocessed reviews (wordcloud + sentiment distribution) ---
df = pd.read_csv("data/processed/reviews_preprocessed.csv").dropna(subset=['clean_text'])
df.to_csv("data/processed/pb_reviews.csv", index=False)
print(f"Saved: pb_reviews.csv ({len(df)} rows)")

# --- 2. Top 30 words ---
all_words = ' '.join(df['clean_text']).split()
word_freq = Counter(all_words).most_common(30)
pd.DataFrame(word_freq, columns=['word', 'count']).to_csv(
    "data/processed/pb_top_words.csv", index=False)
print("Saved: pb_top_words.csv")

# --- 3. Top 20 bigrams ---
bigrams = Counter(ngrams(all_words, 2)).most_common(20)
pd.DataFrame([(' '.join(b), c) for b, c in bigrams],
    columns=['bigram', 'count']).to_csv(
    "data/processed/pb_bigrams.csv", index=False)
print("Saved: pb_bigrams.csv")

# --- 4. Sentiment words (positive vs negative ratio) ---
pos_words = Counter(' '.join(df[df['label'] == 1]['clean_text']).split())
neg_words = Counter(' '.join(df[df['label'] == 0]['clean_text']).split())
all_vocab = set(pos_words) | set(neg_words)

rows = []
for word in all_vocab:
    p = pos_words.get(word, 0)
    n = neg_words.get(word, 0)
    if p + n > 100:
        rows.append({'word': word, 'positive': p, 'negative': n,
                     'ratio': round(p / (p + n), 3),
                     'type': 'positive' if p > n else 'negative'})

pd.DataFrame(rows).sort_values('ratio').to_csv(
    "data/processed/pb_sentiment_words.csv", index=False)
print("Saved: pb_sentiment_words.csv")

# --- 5. Rating trend over time ---
conn = sqlite3.connect("data/processed/reviews.db")
df_time = pd.read_sql("""
    SELECT 
        strftime('%Y', datetime(Time, 'unixepoch')) AS year,
        ROUND(AVG(Score), 2) AS avg_score,
        COUNT(*) AS total_reviews
    FROM amazon_reviews
    GROUP BY year
    ORDER BY year
""", conn)
conn.close()
df_time.to_csv("data/processed/pb_rating_trend.csv", index=False)
print("Saved: pb_rating_trend.csv")

# --- 6. Sentiment distribution ---
dist = df['label'].value_counts().reset_index()
dist.columns = ['label', 'count']
dist['label'] = dist['label'].map({1: 'Positive', 0: 'Negative'})
dist.to_csv("data/processed/pb_sentiment_dist.csv", index=False)
print("Saved: pb_sentiment_dist.csv")

print("\nAll files ready for Power BI!")
print("Import from: data/processed/pb_*.csv")
