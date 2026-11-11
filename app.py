import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Aapke Meta Credentials
ACCESS_TOKEN = (
    "EAAldROaCg6IBS2riGhKiAX8F5c5xKBJPX6CDCZBNR6Enhg99tp2ZC7lFhsWQsPEz4zQkK3WHcnEVcDRIO4lHdSweaDw9k1MIdaqqlQPOSsCZBhHQ1ZAWF2y2d0s0XpEjK7J3w0usxTDCXN4YF2bOhZCZB35yZAt4adW4U5i5zGi6WRUf63osCBHURzj7y1oRxD4f5OJKvoxzlwtTp4CKXfA2sQxX5iKezTaRVswY9wx0ix2gOY7L44yqut0pjRG3D72KNZBXc1x53xB81BuAJmQOhcVfZCm7fQRGLfwZDZD"
)
PHONE_NUMBER_ID = "1429429540258202"
VERIFY_TOKEN = "bank123"


def send_whatsapp(payload):
  url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
  headers = {
      "Authorization": f"Bearer {ACCESS_TOKEN}",
      "Content-Type": "application/json",
  }
  requests.post(url, headers=headers, json=payload)


@app.route("/webhook", methods=["GET"])
def verify():
  mode = request.args.get("hub.mode")
  token = request.args.get("hub.verify_token")
  challenge = request.args.get("hub.challenge")
  if mode == "subscribe" and token == VERIFY_TOKEN:
    return challenge, 200
  return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
  data = request.get_json()
  try:
    entry = data["entry"][0]["changes"][0]["value"]
    if "messages" in entry:
      msg = entry["messages"][0]
      sender = msg["from"]

      # Step 1: User ne bheja 'Hi' -> First Dropdown
      if msg["type"] == "text":
        text = msg["text"]["body"].strip().lower()
        if "hi" in text or "hello" in text:
          payload = {
              "messaging_product": "whatsapp",
              "to": sender,
              "type": "interactive",
              "interactive": {
                  "type": "list",
                  "header": {"type": "text", "text": "Bihar Gramin Bank"},
                  "body": {
                      "text": (
                          "Welcome Priya Singh to BIHAR GRAMIN BANK WhatsApp"
                          " Banking Services 🏦"
                      )
                  },
                  "footer": {"text": "Tap below 👇 to explore All Services"},
                  "action": {
                      "button": "All Services",
                      "sections": [{
                          "title": "Select a Service",
                          "rows": [
                              {
                                  "id": "acc_services",
                                  "title": "Account Related Services",
                                  "description": (
                                      "Check all the account related details"
                                  ),
                              },
                              {
                                  "id": "bank_prod",
                                  "title": "Bank Products",
                                  "description": (
                                      "Inquire Bank's products like deposits"
                                      " scheme, govt. schemes etc."
                                  ),
                              },
                              {
                                  "id": "online_services",
                                  "title": "Online Services",
                                  "description": (
                                      "Check various Online Services offered"
                                      " by Bank"
                                  ),
                              },
                              {
                                  "id": "other_services",
                                  "title": "Other services",
                                  "description": "Locate nearest Branches",
                              },
                          ],
                      }],
                  },
              },
          }
          send_whatsapp(payload)

      # Step 2 & 3: Drop-down List selection
      elif msg["type"] == "interactive":
        interaction = msg["interactive"]

        if interaction["type"] == "list_reply":
          selected_id = interaction["list_reply"]["id"]

          # User clicks Account Related Services
          if selected_id == "acc_services":
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {"type": "text", "text": "Bihar Gramin Bank"},
                    "body": {
                        "text": (
                            "Account Related Services\nCheck all the account"
                            " related details"
                        )
                    },
                    "footer": {"text": "Tap below 👇 to explore All Options"},
                    "action": {
                        "button": "All Services",
                        "sections": [{
                            "title": "Account Options",
                            "rows": [
                                {
                                    "id": "bal_inquiry",
                                    "title": "Balance Inquiry ₹",
                                },
                                {
                                    "id": "last_5_tx",
                                    "title": "Last 5 Transactions 📝",
                                },
                                {
                                    "id": "stop_cheque",
                                    "title": "Stop Cheque 📄",
                                },
                            ],
                        }],
                    },
                },
            }
            send_whatsapp(payload)

          # User clicks Balance Inquiry
          elif selected_id == "bal_inquiry":
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {"type": "text", "text": "Bihar Gramin Bank"},
                    "body": {
                        "text": (
                            "Please select Account number from 👇 below"
                            " list\n\n💡 Tip: Type #menu for Main menu"
                        )
                    },
                    "action": {
                        "button": "A/c Number",
                        "sections": [{
                            "title": "Select Account",
                            "rows": [
                                {
                                    "id": "acc_num_3596",
                                    "title": "7345XXXXXXXX3596",
                                }
                            ],
                        }],
                    },
                },
            }
            send_whatsapp(payload)

          # User clicks Account Number -> Balance + Yes/No Buttons
          elif selected_id == "acc_num_3596":
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                        "text": (
                            "Dear Customer, current available balance in your"
                            " selected Account is *₹ 17572.00*\n\nWould you"
                            " like to know anything else?\nKindly, select an"
                            " option:"
                        )
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {"id": "btn_yes", "title": "Yes"},
                            },
                            {
                                "type": "reply",
                                "reply": {"id": "btn_no", "title": "No"},
                            },
                        ]
                    },
                },
            }
            send_whatsapp(payload)

        # Step 4: Yes/No Buttons
        elif interaction["type"] == "button_reply":
          btn_id = interaction["button_reply"]["id"]

          if btn_id == "btn_no":
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "text",
                "text": {
                    "body": (
                        "Thank you for using our WhatsApp Banking Services!"
                        " Hope we were able to assist you. Please visit"
                        " again!\nTo Restart the conversation, please send 'Hi'"
                    )
                },
            }
            send_whatsapp(payload)

          elif btn_id == "btn_yes":
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "text",
                "text": {
                    "body": (
                        "Please send 'Hi' or select an option from the menu to"
                        " continue."
                    )
                },
            }
            send_whatsapp(payload)

  except Exception as e:
    print(f"Error handling message: {e}")

  return jsonify({"status": "received"}), 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
    
