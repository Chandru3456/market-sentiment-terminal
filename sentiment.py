import pandas as pd
import requests
from textblob import TextBlob
import time

# --- SETUP ---
API_KEY = '99bd177617cc41dd8dc513849b69e06b'  # <--- Paste your key here
QUERY = 'AI AND (Nvidia OR Tech OR Google OR Microsoft)'

def harvest_live_data():
    # 1. Ask the News Server for data
    url = f'https://newsapi.org/v2/everything?q={QUERY}&language=en&sortBy=publishedAt&apiKey={API_KEY}'
    response = requests.get(url).json()
    articles = response.get('articles', [])
    
    # 2. Extract and Analyze each headline
    clean_data = []
    for art in articles[:100]: # Grab the latest 100 news pieces
        title = art['title']
        
        # NLP Analysis: Returns a number between -1 (Very Bad) and 1 (Very Good)
        sentiment_score = TextBlob(title).sentiment.polarity
        
        clean_data.append({
            "PublishedAt": art['publishedAt'],
            "Source": art['source']['name'],
            "Headline": title,
            "SentimentScore": sentiment_score
        })
    
    # 3. Save to CSV (This is the file Power BI will 'watch')
    df = pd.DataFrame(clean_data)
    df.to_csv("tech_news_feed.csv", index=False)
    print(f"Data Harvested at {time.strftime('%H:%M:%S')}")

# --- THE LIVE LOOP ---
while True:
    try:
        harvest_live_data()
        time.sleep(300) # Wait 5 minutes (300 seconds) before doing it again
    except Exception as e:
        print(f"Connection Error: {e}. Retrying in 60 seconds...")
        time.sleep(60)