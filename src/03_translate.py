"""
03_translate.py
---------------
Translates Polish food reviews (degustujemy.pl) to English
using Google Translate via deep-translator library.
Input:  data/raw/degustujemy_scraped.csv
Output: data/raw/degustujemy_translated.csv
"""
import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

df = pd.read_csv("data/raw/degustujemy_scraped.csv", encoding="utf-8")
translator = GoogleTranslator(source="pl", target="en")

def translate_text(text):
    if pd.isna(text) or text == "":
        return None
    try:
        result = translator.translate(str(text)[:500])
        time.sleep(0.3)  # be polite to Google
        return result
    except Exception as e:
        print(f"Translation error: {e}")
        return None

print("Translating titles...")
df["title_en"] = df["title"].apply(translate_text)

print("Translating reviews...")
df["review_text_en"] = df["review_text"].apply(translate_text)

print(f"\nTranslated: {df['review_text_en'].notna().sum()} / {len(df)} rows")
print(df[["title", "title_en"]].head(3))

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/degustujemy_translated.csv", index=False, encoding="utf-8")
print("Saved to data/raw/degustujemy_translated.csv")
