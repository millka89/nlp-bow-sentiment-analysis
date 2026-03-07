"""
05_preprocessing.py
Text preprocessing for NLP/BoW sentiment analysis.
"""

import pandas as pd
import sqlite3
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

# --- Load data ---
conn = sqlite3.connect("data/processed/reviews.db")
df = pd.read_sql("SELECT Score, Text FROM amazon_reviews LIMIT 100000", conn)
conn.close()

# --- Label: positive (1) / negative (0) ---
df = df[df['Score'] != 3]  # delete neutral
df['label'] = df['Score'].apply(lambda x: 1 if x >= 4 else 0)

# --- Clean text ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text) 
    text = re.sub(r'[^a-z\s]', '', text)  # delete numbers and special characters
    return text

# --- Tokenize + remove stopwords + stemming ---
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess(text):
    text = clean_text(text)
    tokens = text.split()
    tokens = [stemmer.stem(w) for w in tokens if w not in stop_words]
    return ' '.join(tokens)

print("Preprocessing...")
df['clean_text'] = df['Text'].astype(str).apply(preprocess)

# --- Save ---
df[['clean_text', 'label']].to_csv("data/processed/reviews_preprocessed.csv", index=False)
print(f"Done! Saved {len(df)} rows.")
print(df[['label', 'clean_text']].head(3))
