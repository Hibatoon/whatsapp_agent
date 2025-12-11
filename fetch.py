import requests
import os
import time
from dotenv import load_dotenv
import google.generativeai as gemini
from google.api_core.exceptions import ResourceExhausted

load_dotenv()
gemini.configure(api_key=os.getenv("GEMINI_API_KEY"))

news_api_key = os.getenv("NEWS_API_KEY")
model = gemini.GenerativeModel("gemini-2.5-flash")

params = {
    'apiKey': news_api_key,
    'country': 'us'
}

response = requests.get("https://newsapi.org/v2/top-headlines", params=params)

if response.status_code == 200:
    data = response.json()

    # Extract only relevant fields to reduce prompt size
    articles = [
        {
            'title': a.get('title'),
            'author': a.get('author'),
            'source': a.get('source', {}).get('name'),
            'description': a.get('description')
        }
        for a in data.get('articles', [])
    ]

    prompt = (
        "Summarize these news articles in bullet-format, and mention:\n"
        "- article title\n"
        "- author\n"
        "- source\n"
        "- short summary\n\n"
        f"Articles:\n{articles}"
    )

    # Retry wrapper for 429 errors
    while True:
        try:
            ai = model.generate_content(prompt)
            print(ai.text)
            break
        except ResourceExhausted as e:
            print("⚠️ Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)

else:
    print(f"Request failed with status code: {response.status_code}")
