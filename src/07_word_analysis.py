"""
07_word_analysis.py
Word frequency analysis: top words, bigrams, trigrams + charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from nltk.util import ngrams
from wordcloud import WordCloud

# --- Load data ---
print("Loading data...")
df = pd.read_csv("data/processed/reviews_preprocessed.csv").dropna(subset=['clean_text'])

all_words = ' '.join(df['clean_text']).split()

# --- Top 20 words ---
word_freq = Counter(all_words).most_common(20)
words, counts = zip(*word_freq)

plt.figure(figsize=(12, 5))
plt.barh(words[::-1], counts[::-1], color='steelblue')
plt.title('Top 20 Most Frequent Words')
plt.xlabel('Frequency')
plt.tight_layout()
plt.savefig('data/processed/top_words.png', dpi=150)
plt.close()
print("Saved: top_words.png")

# --- Top 15 bigrams ---
bigrams = Counter(ngrams(all_words, 2)).most_common(15)
bg_labels = [' '.join(b) for b, _ in bigrams]
bg_counts = [c for _, c in bigrams]

plt.figure(figsize=(12, 5))
plt.barh(bg_labels[::-1], bg_counts[::-1], color='darkorange')
plt.title('Top 15 Bigrams')
plt.xlabel('Frequency')
plt.tight_layout()
plt.savefig('data/processed/top_bigrams.png', dpi=150)
plt.close()
print("Saved: top_bigrams.png")

# --- Top 15 trigrams ---
trigrams = Counter(ngrams(all_words, 3)).most_common(15)
tg_labels = [' '.join(t) for t, _ in trigrams]
tg_counts = [c for _, c in trigrams]

plt.figure(figsize=(12, 5))
plt.barh(tg_labels[::-1], tg_counts[::-1], color='seagreen')
plt.title('Top 15 Trigrams')
plt.xlabel('Frequency')
plt.tight_layout()
plt.savefig('data/processed/top_trigrams.png', dpi=150)
plt.close()
print("Saved: top_trigrams.png")

# --- Word Cloud ---
wc = WordCloud(width=1200, height=600, background_color='white', max_words=200)
wc.generate(' '.join(all_words))
wc.to_file('data/processed/wordcloud.png')
print("Saved: wordcloud.png")

print("\nTop 10 words:", word_freq[:10])
print("Top 5 bigrams:", bigrams[:5])
print("Top 5 trigrams:", trigrams[:5])