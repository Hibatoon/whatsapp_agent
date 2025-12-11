from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

verify_token = os.getenv("VERIFY_TOKEN")

@app.route("/", methods=["GET", "POST"])

def webhook():

    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == verify_token:
            return challenge
        return "Invalid token"

    if request.method == "POST":
        data = request.json
        print("Received:", data)
        return "OK", 200
