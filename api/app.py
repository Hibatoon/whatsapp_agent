from flask import Flask, request
import os
import requests

app = Flask(__name__)

# ---------- ENV VARS ----------
MY_NUMBER = os.getenv("MY_NUMBER")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ---------- BASIC ROUTES ----------
@app.route("/", methods=["GET"])
def index():
    return {"status": "ok"}, 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # ---- VERIFICATION (GET) ----
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid token", 403

    # ---- MESSAGE HANDLING (POST) ----
    if request.method == "POST":
        data = request.json
        print("Received:", data)

        try:
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages")

            if messages:
                msg = messages[0]
                from_number = msg["from"]
                text = msg["text"]["body"]

                reply = f"You said: {text}"
                send_whatsapp(from_number, reply)

        except Exception as e:
            print("Error:", e)

        return "OK", 200


# ---------- DAILY CRON ----------
@app.route("/daily", methods=["GET"])
def daily():
    send_whatsapp(MY_NUMBER, "Daily test message from cron.")
    return {"status": "sent"}, 200


# ---------- SEND WHATSAPP ----------
def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("WA Response:", r.status_code, r.text)


# ---------- REQUIRED FOR VERCEL ----------
def handler(request, response):
    return app(request, response)
