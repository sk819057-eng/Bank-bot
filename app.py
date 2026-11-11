import os
import sys
import json
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Aapka naya Permanent System User Token
ACCESS_TOKEN = "EAAldROaCg6IBS97fVAGfullM9bhjH1nb66ROXElEHnhexFkiWD3CieVlQiRhvn8xixFx0z6dkxMO3hew51zTU2CilP41OprQdQMUDCGeQZCshJCwciyLpiIygTWTTyQwqZBvM2Qxy1eqryFjr9w81IEPtyLHpKTZAfCRWZBeNGs6EhhPtu9dxSIHGrxMZCwZDZD"
PHONE_NUMBER_ID = "1421467811049942"
VERIFY_TOKEN = "bank123"

def send_whatsapp(payload):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"--> META OUTGOING STATUS: {response.status_code}", flush=True)
    print(f"--> META OUTGOING BODY: {response.text}", flush=True)
    return response

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True) or {}
    try:
        entries = data.get('entry', [])
        for entry in entries:
            for change in entry.get('changes', []):
                value = change.get('value', {})
                if 'messages' in value:
                    for msg in value['messages']:
                        sender = msg.get('from')

                        # User sends 'Hi' ya koi bhi text message
                        if msg.get('type') == 'text':
                            payload = {
                                "messaging_product": "whatsapp",
                                "to": sender,
                                "type": "interactive",
                                "interactive": {
                                    "type": "list",
                                    "header": {"type": "text", "text": "Bihar Gramin Bank"},
                                    "body": {"text": "Welcome to BIHAR GRAMIN BANK WhatsApp Banking Services 🏦"},
                                    "footer": {"text": "Tap below 👇 to explore All Services"},
                                    "action": {
                                        "button": "All Services",
                                        "sections": [
                                            {
                                                "title": "Select a Service",
                                                "rows": [
                                                    {"id": "acc_services", "title": "Account Related Services", "description": "Check account details & balance"},
                                                    {"id": "bank_prod", "title": "Bank Products", "description": "Deposits, loans, govt schemes"},
                                                    {"id": "online_services", "title": "Online Services", "description": "Mobile banking, portal links"},
                                                    {"id": "other_services", "title": "Other services", "description": "Branch & ATM locator"}
                                                ]
                                            }
                                        ]
                                    }
                                }
                            }
                            send_whatsapp(payload)

                        # Dropdown Lists Selection
                        elif msg.get('type') == 'interactive':
                            interaction = msg.get('interactive', {})
                            
                            if interaction.get('type') == 'list_reply':
                                selected_id = interaction.get('list_reply', {}).get('id')

                                if selected_id == "acc_services":
                                    payload = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "list",
                                            "header": {"type": "text", "text": "Bihar Gramin Bank"},
                                            "body": {"text": "Account Related Services\nCheck all your account details:"},
                                            "footer": {"text": "Tap below 👇 to explore All Options"},
                                            "action": {
                                                "button": "Account Options",
                                                "sections": [
                                                    {
                                                        "title": "Options",
                                                        "rows": [
                                                            {"id": "bal_inquiry", "title": "Balance Inquiry ₹"},
                                                            {"id": "last_5_tx", "title": "Last 5 Transactions 📝"},
                                                            {"id": "stop_cheque", "title": "Stop Cheque 📄"}
                                                        ]
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                    send_whatsapp(payload)

                                elif selected_id == "bal_inquiry":
                                    payload = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "list",
                                            "header": {"type": "text", "text": "Bihar Gramin Bank"},
                                            "body": {"text": "Please select Account number from 👇 below list\n\n💡 Tip: Type 'Hi' for Main menu"},
                                            "action": {
                                                "button": "A/c Number",
                                                "sections": [
                                                    {
                                                        "title": "Select Account",
                                                        "rows": [
                                                            {"id": "acc_num_3596", "title": "7345XXXXXXXX3596"}
                                                        ]
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                    send_whatsapp(payload)

                                elif selected_id == "acc_num_3596":
                                    # Message 1: Exact balance text
                                    balance_msg = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "text",
                                        "text": {
                                            "body": "Dear Customer, current available balance in your selected Account is *₹ 27572.00"
                                        }
                                    }
                                    send_whatsapp(balance_msg)

                                    time.sleep(0.5)

                                    # Message 2: Yes / No Option Buttons
                                    followup_msg = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "button",
                                            "body": {
                                                "text": "Would you like to know anything else?\nKindly, select an option:"
                                            },
                                            "action": {
                                                "buttons": [
                                                    {"type": "reply", "reply": {"id": "btn_yes", "title": "Yes"}},
                                                    {"type": "reply", "reply": {"id": "btn_no", "title": "No"}}
                                                ]
                                            }
                                        }
                                    }
                                    send_whatsapp(followup_msg)

                            # Button replies (Yes / No)
                            elif interaction.get('type') == 'button_reply':
                                btn_id = interaction.get('button_reply', {}).get('id')

                                if btn_id == "btn_no":
                                    payload = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "text",
                                        "text": {"body": "Thank you for using Bihar Gramin Bank WhatsApp Banking Services! Have a great day.\nTo start again, send 'Hi'."}
                                    }
                                    send_whatsapp(payload)

                                elif btn_id == "btn_yes":
                                    payload = {
                                        "messaging_product": "whatsapp",
                                        "to": sender,
                                        "type": "text",
                                        "text": {"body": "Kripya 'Hi' bhejein main menu par wapas jaane ke liye."}
                                    }
                                    send_whatsapp(payload)

    except Exception as e:
        print(f"--> ERROR PROCESSING: {str(e)}", flush=True)

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
