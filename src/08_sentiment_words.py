"""
08_sentiment_words.py
Words characteristic for positive vs negative reviews + correlation with rating.
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# --- Load data ---
print("Loading data...")
df = pd.read_csv("data/processed/reviews_preprocessed.csv").dropna(subset=['clean_text'])

pos = df[df['label'] == 1]['clean_text']
neg = df[df['label'] == 0]['clean_text']

pos_words = Counter(' '.join(pos).split())
neg_words = Counter(' '.join(neg).split())

# --- Top 20 words unique to positive / negative ---
all_words = set(pos_words) | set(neg_words)
scores = {}
for word in all_words:
    p = pos_words.get(word, 0)
    n = neg_words.get(word, 0)
    if p + n > 100:  # min frequency filter
        scores[word] = p / (p + n)  # ratio: higher = more positive

sorted_words = sorted(scores.items(), key=lambda x: x[1])
top_neg = sorted_words[:20]   # most negative
top_pos = sorted_words[-20:]  # most positive

# --- Butterfly chart ---
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Negative words
neg_labels = [w for w, _ in top_neg]
neg_vals = [scores[w] for w, _ in top_neg]
axes[0].barh(neg_labels, neg_vals, color='tomato')
axes[0].set_title('Most Negative Words')
axes[0].set_xlabel('Positive ratio (lower = more negative)')
axes[0].set_xlim(0, 1)

# Positive words
pos_labels = [w for w, _ in top_pos[::-1]]
pos_vals = [scores[w] for w, _ in top_pos[::-1]]
axes[1].barh(pos_labels, pos_vals, color='steelblue')
axes[1].set_title('Most Positive Words')
axes[1].set_xlabel('Positive ratio (higher = more positive)')
axes[1].set_xlim(0, 1)

plt.suptitle('Words Characteristic for Positive vs Negative Reviews', fontsize=14)
plt.tight_layout()
plt.savefig('data/processed/sentiment_words.png', dpi=150)
plt.close()
print("Saved: sentiment_words.png")

# --- Print top words ---
print("\nTop 10 most NEGATIVE words:")
for word, ratio in top_neg[:10]:
    print(f"  {word}: {ratio:.2f} positive ratio")

print("\nTop 10 most POSITIVE words:")
for word, ratio in top_pos[-10:][::-1]:
    print(f"  {word}: {ratio:.2f} positive ratio")
