import requests
import os
from dotenv import load_dotenv

load_dotenv()

phone_number_id = os.getenv("PHONE_NUMBER_ID")
whatsapp_access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")

# print(whatsapp_access_token)

url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
headers = {
    "Authorization": f"Bearer {whatsapp_access_token}",
    "Content-Type": "application/json"
}
# 
payload = {
    "messaging_product": "whatsapp",
    "to": "212695473484",
    "type": "text",
    "text": {"body": "Hello from WhatsApp Cloud API!"}
}
# 
response = requests.post(url, headers=headers, json=payload)
print(response.json())
