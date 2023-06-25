from flask import Flask, request
import requests


app = Flask(__name__)

# sending request
token = "YOUR_TOKEN"

# verify webhook
mytoken = "YOUR_VERIFY_TOKEN"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    verify_token = request.args.get("hub.verify_token")

    if mode and verify_token:
        if mode == "subscribe" and verify_token == mytoken:
            return challenge, 200
        else:
            return "", 403

@app.route("/webhook", methods=["POST"])
def process_webhook():
    body_param = request.get_json()

    if body_param.get("object"):
        if (
            body_param.get("entry")
            and body_param["entry"][0].get("changes")
            and body_param["entry"][0]["changes"][0].get("value")
            and body_param["entry"][0]["changes"][0]["value"].get("messages")
            and body_param["entry"][0]["changes"][0]["value"]["messages"][0]
        ):
            phone_no_id = body_param["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            sender = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            message_body = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

            # token which you used to send message to the user
            response = requests.post(
                f"https://graph.facebook.com/v17.0/{phone_no_id}/messages?access_token={token}",
                json={
                    "messaging_product": "whatsapp",
                    "to": sender,
                    "text": {
                        "body": "Hi.. I'm asif"
                    }
                },
                headers={
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                return "", 200
            else:
                return "", 500
        else:
            return "", 404

@app.route("/", methods=["GET"])
def hello():
    return "hello there", 200

if __name__ == "__main__":
    app.run(port=8000)
