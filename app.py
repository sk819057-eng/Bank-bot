import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Aapke Meta Credentials
ACCESS_TOKEN = "EAAldROaCg6IBS9ZAlFegLSf7jn9bSknu8Dxl6ZBtbyNFFwnDWsf6kBAjtVVZBQ4UaL0oG7kLPZCbvqPRBumZAGYqXmrheYZBrtfi0zZB9s22dGfIZCY8H5yI8EHZBJjqbGI3ASSZAgCbgYUuMHQqxphURoGKJR43LIqBgZBNqZBfxzCIagBAbA51tPVXlizZCuZBmXmXRIhzRz6EY1VwNW6dugI8ZBWVh0FZCRBfyWbCfnBGf5s6fYF4qDZACRHwp221cjNLZAeefyBemMnjydactFe6fDoG9fLI4ZCI7V1HbQsMWQZD"
PHONE_NUMBER_ID = "1421467811049942"
VERIFY_TOKEN = "bank123"

def send_whatsapp(payload):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    requests.post(url, headers=headers, json=payload)

@app.route('/webhook', methods=['GET'])
def verify():
    # Meta webhook verification challenge
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            sender = msg['from']
            
            # Step 1: User ne bheja 'Hi' -> First Dropdown
            if msg['type'] == 'text':
                text = msg['text']['body'].strip().lower()
                if 'hi' in text or 'hello' in text:
                    payload = {
                        "messaging_product": "whatsapp",
                        "to": sender,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {"type": "text", "text": "Bihar Gramin Bank"},
                            "body": {"text": "Welcome Priya Singh to BIHAR GRAMIN BANK WhatsApp Banking Services 🏦"},
                            "footer": {"text": "Tap below 👇 to explore All Services"},
                            "action": {
                                "button": "All Services",
                                "sections": [{
                                    "title": "Select a Service",
                                    "rows": [
                                        {"id": "acc_services", "title": "Account Related Services", "description": "Check all the account related details"},
                                        {"id": "bank_prod", "title": "Bank Products", "description": "Inquire Bank's products like deposits scheme, govt. schemes etc."},
                                        {"id": "online_services", "title": "Online Services", "description": "Check various Online Services offered by Bank"},
                                        {"id": "other_services", "title": "Other services", "description": "Locate nearest Branches"}
                                    ]
                                }]
                            }
                        }
                    }
                    send_whatsapp(payload)

            # Step 2 & 3: Drop-down Selection Handle
            elif msg['type'] == 'interactive':
                interaction = msg['interactive']
                
                if interaction['type'] == 'list_reply':
                    selected_id = interaction['list_reply']['id']
                    
                    # 2. Account Related Services par click kiya
                    if selected_id == "acc_services":
                        payload = {
                            "messaging_product": "whatsapp",
                            "to": sender,
                            "type": "interactive",
                            "interactive": {
                                "type": "list",
                                "header": {"type": "text", "text": "Bihar Gramin Bank"},
                                "body": {"text": "Account Related Services\nCheck all the account related details"},
                                "footer": {"text": "Tap below 👇 to explore All Options"},
                                "action": {
                                    "button": "All Services",
                                    "sections": [{
                                        "title": "Account Options",
                                        "rows":
                                         
