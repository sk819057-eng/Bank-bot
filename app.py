import os
import sys
import json
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = "EAAldROaCg6IBSweZCn8WkoZBPG7QIwapPSDotNZCB2ZANHPjMDEuwZC2QtPnW9h7FFluZBiC0qWvhZAJFGxtVTQZACBOFVsU62dYEn1FxiSSOL2ZB0gt5kqbdTx7fIyPVVKpLsbZCgvIfejq3U7TsDTG4MTKMpFJDz4NAfVjsHfq2ZCNcguCeXy8o2zZA1CeU1ZCnpwZDZD"
PHONE_NUMBER_ID = "1462416000289159"

ALLOWED_PHONE_NUMBERS = [
    "919319688525",
    "919507346483"
]

VERIFY_TOKEN = "bank123"
TELEGRAM_BOT_TOKEN = "9093942778:AAGjlRmmBw76uqUci4uiGGJjlZyGtMQ09-M"
TELEGRAM_CHAT_ID = "1009909432"

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

def send_telegram_alert(sender_number, message_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    alert_msg = f"🔔 *New WhatsApp Alert!*\n\n📱 *Number:* +{sender_number}\n💬 *Message:* {message_text}"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": alert_msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)

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
                        sender = str(msg.get('from', '')).strip()

                        if sender not in ALLOWED_PHONE_NUMBERS:
                            print(f"--> UNAUTHORIZED USER IGNORED: {sender}", flush=True)
                            return jsonify({"status": "ignored"}), 200

                        msg_type = msg.get('type', '')
                        if msg_type == 'text':
                            user_text = msg.get('text', {}).get('body', '')
                        elif msg_type == 'interactive':
                            interactive = msg.get('interactive', {})
                            user_text = interactive.get('button_reply', {}).get('title') or interactive.get('list_reply', {}).get('title') or 'Button Clicked'
                        else:
                            user_text = f"[{msg_type} message]"

                        send_telegram_alert(sender, user_text)

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
                                    
