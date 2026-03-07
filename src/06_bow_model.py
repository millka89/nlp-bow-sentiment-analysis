"""
06_bow_model.py
Bag of Words sentiment classification using TF-IDF + Logistic Regression.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# --- Load preprocessed data ---
print("Loading data...")
df = pd.read_csv("data/processed/reviews_preprocessed.csv")
df = df.dropna(subset=['clean_text'])

# --- Split ---
X_train, X_test, y_train, y_test = train_test_split(
    df['clean_text'], df['label'], test_size=0.2, random_state=42
)

# --- TF-IDF Vectorization ---
print("Vectorizing...")
vectorizer = TfidfVectorizer(max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --- Train model ---
print("Training model...")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vec, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test_vec)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))