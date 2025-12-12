# # from flask import Flask, request, jsonify
# # import os
# # import requests
# # import google.generativeai as genai

# # app = Flask(__name__)

# # MY_NUMBER = os.getenv("MY_NUMBER")
# # WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# # PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
# # VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# # model = None
# # if GEMINI_API_KEY:
# #     genai.configure(api_key=GEMINI_API_KEY)
# #     model = genai.GenerativeModel("gemini-1.5-flash")

# # def fetch_news():
# #     """
# #     Fetches top headlines from NewsAPI and formats them for WhatsApp.
# #     Returns a formatted string with the news articles.
# #     """
# #     if not NEWS_API_KEY:
# #         return "❌ News API key not configured. Please set NEWS_API_KEY environment variable."
    
# #     try:
# #         # NewsAPI endpoint for top headlines
# #         url = "https://newsapi.org/v2/top-headlines"
# #         params = {
# #             "apiKey": NEWS_API_KEY,
# #             "language": "en",
# #             "pageSize": 3  # only 3 articles
# #         }

        
# #         response = requests.get(url, params=params, timeout=5)
# #         response.raise_for_status()  # Raise exception for bad status codes
        
# #         data = response.json()
        
# #         # Check if request was successful
# #         if data.get("status") != "ok":
# #             return f"❌ News API error: {data.get('message', 'Unknown error')}"
        
# #         articles = data.get("articles", [])
        
# #         if not articles:
# #             return "📰 No news articles found today."
        
# #         # Format news for WhatsApp
# #         news_message = "📰 *Today's Top News*\n\n"
        
# #         for i, article in enumerate(articles, start=1):
# #             title = article.get("title", "No title")
# #             source = article.get("source", {}).get("name", "Unknown source")
# #             url = article.get("url", "")
# #             description = article.get("description", "")
            
# #             # Format each article
# #             news_message += f"*{i}. {title}*\n"
# #             news_message += f"_{source}_\n"
            
# #             # Add description if available (truncate if too long)
# #             if description:
# #                 desc = description[:100] + "..." if len(description) > 100 else description
# #                 news_message += f"{desc}\n"
            
# #             # Add URL if available
# #             if url:
# #                 news_message += f"🔗 {url}\n"
            
# #             news_message += "\n"
        
# #         return news_message.strip()
        
# #     except requests.exceptions.Timeout:
# #         return "❌ Request timeout. News service is taking too long to respond."
# #     except requests.exceptions.RequestException as e:
# #         print(f"News API request error: {e}")
# #         if hasattr(e, 'response') and e.response is not None:
# #             try:
# #                 error_data = e.response.json()
# #                 return f"❌ News API error: {error_data.get('message', 'Unknown error')}"
# #             except:
# #                 return f"❌ News API error: HTTP {e.response.status_code}"
# #         return f"❌ Error fetching news: {str(e)}"
# #     except Exception as e:
# #         print(f"Unexpected error in fetch_news: {e}")
# #         return f"❌ Unexpected error: {str(e)}"

# # @app.route("/", methods=["GET"])
# # def index():
# #     return {"status": "ok"}, 200

# # @app.route("/webhook", methods=["GET", "POST"])
# # def webhook():
# #     if request.method == "GET":
# #         token = request.args.get("hub.verify_token")
# #         challenge = request.args.get("hub.challenge")
# #         if token == VERIFY_TOKEN:
# #             return challenge
# #         return "Invalid token", 403

# #     if request.method == "POST":
# #         data = request.json
# #         print("Received:", data)

# #         try:
# #             entry = data["entry"][0]
# #             changes = entry["changes"][0]
# #             value = changes["value"]
# #             messages = value.get("messages")

# #             if messages:
# #                 message = messages[0]
# #                 from_number = message["from"]
# #                 text = message["text"]["body"]

# #                 reply = generate_reply(text)
# #                 send_whatsapp_message(from_number, reply)

# #         except Exception as e:
# #             print("Error parsing message:", e)

# #         return "OK", 200

# # def generate_reply(text):
# #     try:
# #         response = model.generate_content(f"Respond shortly to: {text}")
# #         return response.text
# #     except:
# #         return "Error generating reply."

# # def send_whatsapp_message(to, text):
# #     try:
# #         url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"
# #         headers = {
# #             "Authorization": f"Bearer {WHATSAPP_TOKEN}",
# #             "Content-Type": "application/json"
# #         }
# #         payload = {
# #             "messaging_product": "whatsapp",
# #             "to": to,
# #             "text": {"body": text[:4000]}  # truncate if too long
# #         }
# #         r = requests.post(url, headers=headers, json=payload, timeout=5)
# #         print("WA Response:", r.status_code, r.text)
# #     except Exception as e:
# #         print("Error sending WhatsApp message:", e)


# # @app.route("/daily", methods=["GET"])
# # def daily_message():
# #     try:
# #         msg = fetch_news()

# #         # Truncate or fallback
# #         if not msg:
# #             msg = "📰 Couldn't fetch news today."

# #         # Split if too long
# #         for chunk in [msg[i:i+4000] for i in range(0, len(msg), 4000)]:
# #             send_whatsapp_message(MY_NUMBER, chunk)

# #         return {"status": "news_sent"}, 200

# #     except Exception as e:
# #         print("Daily job error:", e)
# #         return {"error": "Daily job failed"}, 200


# from flask import Flask, request, jsonify
# import os
# import requests
# import google.generativeai as genai

# app = Flask(__name__)

# # Environment variables
# MY_NUMBER = os.getenv("MY_NUMBER")
# WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
# VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# # Configure Gemini
# model = None
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
#     model = genai.GenerativeModel("gemini-2.5-flash")  # latest stable

# # ========================
# # News fetching
# # ========================
# def fetch_news():
#     """Fetch top 3 headlines from NewsAPI and format for WhatsApp."""
#     if not NEWS_API_KEY:
#         return "❌ News API key not configured."
#     try:
#         url = "https://newsapi.org/v2/top-headlines"
#         params = {
#             "apiKey": NEWS_API_KEY,
#             "language": "en",
#             "pageSize": 3
#         }
#         r = requests.get(url, params=params, timeout=5)
#         r.raise_for_status()
#         data = r.json()
#         if data.get("status") != "ok":
#             return f"❌ News API error: {data.get('message', 'Unknown error')}"
#         articles = data.get("articles", [])
#         if not articles:
#             return "📰 No news articles found today."

#         msg = "📰 *Today's Top News*\n\n"
#         for i, art in enumerate(articles, start=1):
#             title = art.get("title", "No title")
#             src = art.get("source", {}).get("name", "Unknown")
#             url = art.get("url", "")
#             desc = art.get("description", "")
#             msg += f"*{i}. {title}*\n_{src}_\n"
#             if desc:
#                 desc_short = desc[:100] + "..." if len(desc) > 100 else desc
#                 msg += f"{desc_short}\n"
#             if url:
#                 msg += f"🔗 {url}\n"
#             msg += "\n"
#         return msg.strip()
#     except Exception as e:
#         print("Error fetching news:", e)
#         return "❌ Couldn't fetch news today."

# # ========================
# # WhatsApp messaging
# # ========================
# def send_whatsapp_message(to, text):
#     """Send message via WhatsApp API (safe for Vercel)."""
#     try:
#         # Split into chunks if too long
#         for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
#             url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"
#             headers = {
#                 "Authorization": f"Bearer {WHATSAPP_TOKEN}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "messaging_product": "whatsapp",
#                 "to": to,
#                 "text": {"body": chunk}
#             }
#             r = requests.post(url, headers=headers, json=payload, timeout=5)
#             print("WA response:", r.status_code, r.text)
#     except Exception as e:
#         print("Error sending WhatsApp message:", e)

# # ========================
# # Gemini replies
# # ========================
# def generate_reply(text):
#     if not model:
#         return "Error: Gemini API not configured."
#     try:
#         resp = model.generate_content(f"Reply concisely to: {text}")
#         if hasattr(resp, "text") and resp.text:
#             return resp.text
#         if hasattr(resp, "response") and resp.response:
#             return resp.response[0].content
#         return "Sorry, couldn't generate a reply."
#     except Exception as e:
#         print("Gemini error:", e)
#         return "Error generating reply."

# # ========================
# # Routes
# # ========================
# @app.route("/", methods=["GET"])
# def index():
#     return {"status": "ok"}, 200

# @app.route("/webhook", methods=["GET", "POST"])
# def webhook():
#     if request.method == "GET":
#         token = request.args.get("hub.verify_token")
#         challenge = request.args.get("hub.challenge")
#         if token == VERIFY_TOKEN:
#             return challenge
#         return "Invalid token", 403

#     if request.method == "POST":
#         try:
#             data = request.json
#             print("Received:", data)
#             entry = data.get("entry", [])[0]
#             changes = entry.get("changes", [])[0]
#             value = changes.get("value", {})
#             messages = value.get("messages", [])
#             if messages:
#                 msg = messages[0]
#                 from_number = msg.get("from")
#                 text = msg.get("text", {}).get("body", "")
#                 reply = generate_reply(text)
#                 send_whatsapp_message(from_number, reply)
#         except Exception as e:
#             print("Error handling webhook message:", e)
#         return "OK", 200

# @app.route("/daily", methods=["GET"])
# def daily_message():
#     try:
#         news_msg = fetch_news()

#         send_whatsapp_message(MY_NUMBER, news_msg)
#         return {"status": "news_sent"}, 200
#     except Exception as e:
#         print("Error in daily message:", e)
#         return {"error": "Daily job failed"}, 200

# # Vercel serverless handler
# # handler = app


# **********************************************

"""
WhatsApp AI News Agent - Richdale AI PFE Assessment
Single-file Flask app for daily news summaries and real-time requests
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN') or os.getenv('WHATSAPP_TOKEN')
WHATSAPP_VERIFY_TOKEN = os.getenv('VERIFY_TOKEN') or os.getenv('WHATSAPP_VERIFY_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID') or os.getenv('PHONE_NUMBER_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MY_NUMBER = os.getenv('MY_NUMBER')

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# Store user phone numbers for daily broadcast (in production, use a database)
SUBSCRIBERS = set()


def fetch_news(category=None, country='us', page_size=10):
    """Fetch news from NewsAPI"""
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country,
        'pageSize': page_size
    }
    
    if category and category.lower() in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
        params['category'] = category.lower()
    
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            return data.get('articles', [])
        return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def summarize_with_gemini(articles, style="France 24 / 2M inspired"):
    """Summarize news articles using Gemini API"""
    if not articles:
        return "No news articles available at the moment."
    
    # Prepare articles summary for LLM
    news_text = ""
    for idx, article in enumerate(articles[:8], 1):  # Limit to 8 articles
        title = article.get('title', 'No title')
        description = article.get('description', '')
        source = article.get('source', {}).get('name', 'Unknown')
        news_text += f"{idx}. {title}\n   Source: {source}\n   {description}\n\n"
    
    prompt = f"""You are a professional news editor for {style} news format.

Summarize the following news articles into clean, concise bullet points. Each bullet should:
- Start with an emoji related to the topic
- Be informative and engaging
- Include the source in parentheses
- Be written in a professional journalistic tone
- Maximum 2 lines per bullet

News articles:
{news_text}

Provide exactly 5-8 bullet points covering the most important stories."""

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        summary = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        
        if summary:
            return summary.strip()
        return "Unable to generate summary at this time."
        
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback to basic formatting
        return format_news_basic(articles[:5])


def format_news_basic(articles):
    """Basic news formatting as fallback"""
    if not articles:
        return "No news available."
    
    formatted = "📰 *Latest News Headlines*\n\n"
    for idx, article in enumerate(articles, 1):
        title = article.get('title', 'No title')
        source = article.get('source', {}).get('name', 'Unknown')
        formatted += f"{idx}. {title}\n   _({source})_\n\n"
    return formatted


def send_whatsapp_message(to_phone, message_text):
    """Send WhatsApp message via Cloud API"""
    if not WHATSAPP_ACCESS_TOKEN:
        print("Error: WHATSAPP_ACCESS_TOKEN not configured")
        return None
    if not WHATSAPP_PHONE_NUMBER_ID:
        print("Error: WHATSAPP_PHONE_NUMBER_ID not configured")
        return None
    if not to_phone:
        print("Error: to_phone is empty")
        return None
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message_text}
    }
    
    try:
        print(f"Sending WhatsApp message to {to_phone}")
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload, timeout=10)
        print(f"WhatsApp API response status: {response.status_code}")
        print(f"WhatsApp API response: {response.text}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None


def process_user_message(message_text, user_phone):
    """Process incoming user messages and generate responses"""
    message_lower = message_text.lower().strip()
    
    # Add user to subscribers
    SUBSCRIBERS.add(user_phone)
    
    # Command parsing
    if 'news' in message_lower:
        # Extract category
        category_map = {
            'tech': 'technology',
            'technology': 'technology',
            'business': 'business',
            'economy': 'business',
            'world': 'general',
            'health': 'health',
            'sports': 'sports',
            'science': 'science',
            'entertainment': 'entertainment'
        }
        
        category = None
        for key, value in category_map.items():
            if key in message_lower:
                category = value
                break
        
        # Fetch and summarize news
        articles = fetch_news(category=category, page_size=8)
        
        if articles:
            category_text = f" {category.upper()}" if category else ""
            header = f"📰 *TODAY'S{category_text} NEWS*\n"
            header += f"_{datetime.now().strftime('%B %d, %Y - %H:%M')}_\n\n"
            
            summary = summarize_with_gemini(articles)
            response = header + summary
        else:
            response = "⚠️ Unable to fetch news at the moment. Please try again later."
    
    elif 'subscribe' in message_lower:
        response = "✅ You're subscribed to daily news at 20:00 UTC!"
    
    elif 'help' in message_lower or message_lower == 'hi' or message_lower == 'hello':
        response = """👋 *Welcome to AI News Agent!*

I can help you with:

📰 *News Commands:*
• "news" - General top headlines
• "news tech" - Technology news
• "news world" - International news
• "news business" or "news economy"
• "news sports"
• "news health"
• "news science"

⏰ *Daily Summary:*
I automatically send news summaries at 20:00 UTC daily!

Type any command to get started."""
    
    else:
        response = "🤔 I didn't understand that. Try:\n• 'news tech'\n• 'news world'\n• 'help' for more options"
    
    return response


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """WhatsApp webhook endpoint"""
    
    if request.method == 'GET':
        # Webhook verification
        verify_token = request.args.get('hub.verify_token', '').strip()
        challenge = request.args.get('hub.challenge', '').strip()
        mode = request.args.get('hub.mode', '').strip()
        
        expected_token = (WHATSAPP_VERIFY_TOKEN or '').strip()
        
        print(f"Webhook verification attempt - mode: {mode}, token received: '{verify_token}', expected: '{expected_token}'")
        
        if mode == 'subscribe' and verify_token and verify_token == expected_token:
            print(f"Webhook verified successfully")
            return str(challenge), 200
        else:
            print(f"Webhook verification failed")
            return 'Invalid verification token', 403
    
    elif request.method == 'POST':
        # Handle incoming messages
        data = request.get_json()
        
        try:
            # Extract message data
            entry = data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [])
            
            if messages:
                message = messages[0]
                from_phone = message.get('from')
                message_type = message.get('type')
                
                if message_type == 'text':
                    message_text = message.get('text', {}).get('body', '')
                    
                    # Process message and generate response
                    response_text = process_user_message(message_text, from_phone)
                    
                    # Send reply
                    send_whatsapp_message(from_phone, response_text)
            
            return jsonify({"status": "success"}), 200
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/send_daily_news', methods=['GET', 'POST'])
def send_daily_news():
    """
    Cron-triggered endpoint to send daily news summary
    This should be called by Vercel Cron at 20:00 UTC
    """
    try:
        # Fetch top news
        articles = fetch_news(category=None, page_size=10)
        
        if not articles:
            return jsonify({"status": "error", "message": "No articles found"}), 500
        
        # Generate summary
        header = f"🌍 *DAILY NEWS DIGEST*\n"
        header += f"_{datetime.now().strftime('%B %d, %Y - 20:00 UTC')}_\n\n"
        
        summary = summarize_with_gemini(articles)
        message = header + summary + "\n\n_Reply 'news tech', 'news world', etc. for more specific updates!_"
        
        # Send to MY_NUMBER (your configured number)
        if not MY_NUMBER:
            return jsonify({"status": "error", "message": "MY_NUMBER not configured"}), 500
        
        result = send_whatsapp_message(MY_NUMBER, message)
        
        if result:
            return jsonify({
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "sent_to": MY_NUMBER,
                "message_preview": message[:100] + "..."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to send WhatsApp message"
            }), 500
        
    except Exception as e:
        print(f"Error in send_daily_news: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "WhatsApp AI News Agent",
        "subscribers": len(SUBSCRIBERS)
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API info"""
    return jsonify({
        "service": "WhatsApp AI News Agent",
        "version": "1.0.0",
        "endpoints": {
            "/webhook": "WhatsApp webhook (GET for verification, POST for messages)",
            "/send_daily_news": "Trigger daily news broadcast (GET/POST)",
            "/health": "Health check"
        },
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    # For local testing
    app.run(debug=True, port=5000)