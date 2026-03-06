# 🔍 NLP Sentiment Analysis — Bag of Words

Analiza opinii klientów Amazon z wykorzystaniem metody Bag of Words
w celu identyfikacji najczęstszych tematów i sentymentu.

## 🛠️ Tech Stack
- **Python** — pandas, nltk, scikit-learn
- **SQL** — SQLite
- **BI** — Power BI / Plotly Dash
- **API** — Kaggle API

## 📊 Wyniki
![Wordcloud](outputs/wordcloud.png)

## 🚀 Jak uruchomić
1. Sklonuj repo: `git clone ...`
2. Zainstaluj biblioteki: `pip install -r requirements.txt`
3. Dodaj plik `.env` z tokenem Kaggle
4. Uruchom: `python src/01_download.py`

## 📁 Struktura projektu
nlp-bow-sentiment-analysis/
│
├── .env                  ← token (prywatny, w .gitignore!)
├── .gitignore
├── README.md             ← opis projektu (ważny dla portfolio!)
├── requirements.txt      ← lista bibliotek
│
├── data/                 ← w .gitignore (za duże pliki)
│   └── Reviews.csv
│
├── notebooks/            ← eksploracja, EDA
│   └── 00_exploration.ipynb
│
├── src/                  ← główny kod
│   ├── 01_download.py
│   ├── 02_sql.py
│   ├── 03_nlp.py
│   └── 04_dashboard.py
│
└── outputs/              ← wykresy, wyniki
    └── wordcloud.png
