import streamlit as st
import yfinance as yf
import requests
from fuzzywuzzy import process
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Set your NewsAPI key here
NEWS_API_KEY = "your_newsapi_key_here"

# List of available tickers
available_tickers = [
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'HDB', 'HDFCBANK.NS', 'VODAFONE', 'BABA', 
    'SPY', 'NFLX', 'BA', 'DIS', 'NVDA', 'JPM', 'WMT', 'HSBC', 'TCS.NS', 'INFY.NS', 'STX'
]

# Match ticker
def get_best_matching_ticker(company_name):
    matched_ticker, score = process.extractOne(company_name.upper(), available_tickers)
    return matched_ticker if score >= 75 else None

# Fetch stock data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1mo")

# Use NewsAPI to fetch top headlines
def fetch_news_articles(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            headlines = [article['title'] for article in articles[:5]]  # Top 5 headlines
            return headlines
        else:
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# Analyze sentiment
def analyze_sentiment(headlines):
    sid = SentimentIntensityAnalyzer()
    sentiments = [sid.polarity_scores(headline)['compound'] for headline in headlines]
    return sentiments

# Plot stock prices
def plot_stock_data(df):
    st.subheader("📈 Stock Price - Last 1 Month")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df['Close'], label="Close Price", color='blue')
    ax.set_title("Stock Trend")
    ax.set_ylabel("Price (USD)")
    ax.set_xlabel("Date")
    ax.grid(True)
    st.pyplot(fig)

# Predict trend based on sentiment and stock
def predict_trend(df, sentiments):
    if not sentiments:
        return "⚠ Not enough data", "No news headlines available to evaluate sentiment."

    price_diff = df['Close'].iloc[-1] - df['Close'].iloc[0]
    avg_sentiment = sum(sentiments) / len(sentiments)

    if price_diff > 0 and avg_sentiment > 0.2:
        return "📈 Positive", f"Price increased by {price_diff:.2f} and sentiment is positive ({avg_sentiment:.2f})"
    elif price_diff < 0 and avg_sentiment < -0.2:
        return "📉 Negative", f"Price dropped by {price_diff:.2f} and sentiment is negative ({avg_sentiment:.2f})"
    else:
        return "➖ Neutral", f"Price changed by {price_diff:.2f}, sentiment is {avg_sentiment:.2f}"

# Streamlit App
def main():
    st.set_page_config(page_title="Stock Sentiment Analyzer", layout="centered")
    st.title("📊 Stock Sentiment Analyzer")

    company = st.text_input("🔎 Enter Stock Ticker or Company Name (e.g., AAPL, TSLA, MSFT):")

    if company:
        with st.spinner("Fetching data and analyzing sentiment..."):
            try:
                ticker = get_best_matching_ticker(company)
                if ticker is None:
                    st.error("❌ Could not find a matching ticker. Try again.")
                    return

                st.success(f"Using Ticker: {ticker}")

                stock_df = fetch_stock_data(ticker)
                if stock_df.empty:
                    st.error("❌ No stock data found.")
                    return

                plot_stock_data(stock_df)

                st.subheader("📰 Latest News & Sentiment")
                headlines = fetch_news_articles(company)
                if headlines:
                    sentiments = analyze_sentiment(headlines)
                    for i, headline in enumerate(headlines):
                        st.markdown(f"**{headline}**")
                        st.markdown(f"Sentiment Score: `{sentiments[i]:.2f}`")
                        st.markdown("---")
                else:
                    st.warning("No recent news found.")
                    sentiments = []

                st.subheader("🔮 Prediction Based on Trend & Sentiment")
                trend, reason = predict_trend(stock_df, sentiments)
                st.markdown(f"**Prediction**: {trend}")
                st.markdown(f"**Reason**: {reason}")

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == '__main__':
    main()