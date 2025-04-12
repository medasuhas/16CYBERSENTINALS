
---

```markdown
# 📊 Stock Sentiment Analyzer

This Streamlit web application allows users to analyze the **stock trend and news sentiment** of a company using real-time market data and recent news articles. It combines stock price analysis with sentiment analysis from news headlines to predict a stock's overall trend.

---

## 🔧 Features

- 🔍 Input stock ticker or company name (e.g., AAPL, TSLA)
- ✅ Fuzzy matching for ticker suggestions
- 📈 Stock price trend visualization (1-month history)
- 📰 Fetches latest news headlines from NewsAPI
- 🧠 Sentiment analysis using VADER
- 🔮 Trend prediction based on price movement and news sentiment

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stock-sentiment-analyzer.git
cd stock-sentiment-analyzer
```

### 2. Install Required Packages

Make sure you have Python installed (version 3.7 or higher).

Install all required libraries:

```bash
pip install fuzzywuzzy
pip install python-Levenshtein  # Optional: To speed up fuzzy matching
pip install streamlit yfinance beautifulsoup4 requests nltk matplotlib seaborn
```

Also, download the VADER lexicon for sentiment analysis:

```python
import nltk
nltk.download('vader_lexicon')
```

---

## 🔑 News API Key

This app uses the [NewsAPI](https://newsapi.org/) to fetch recent headlines.

To run the app, you'll need an API key:

1. Sign up at [https://newsapi.org/](https://newsapi.org/)
2. Get your API key
3. Replace the placeholder in `stock.py`:

```python
NEWS_API_KEY = "your_newsapi_key_here"
```

---

## 💻 Run the App

From your terminal or command prompt:

```bash
streamlit run stock.py
```

---

## 📁 Files Included

- `stock.py`: Main Streamlit application code
- `Untitled1.ipynb`: (Optional) Jupyter Notebook version or experiments

---

## 📸 Demo

<img src="demo.png" alt="Demo Screenshot" width="600"/>

---

## 🙌 Credits

Developed using:
- Streamlit
- yFinance
- NewsAPI
- VADER Sentiment Analyzer
- FuzzyWuzzy for fuzzy matching
- Matplotlib

---



This project is open-source and free to use under the MIT License.
```

---

Let me know if you’d like me to create a `requirements.txt` file as well!
