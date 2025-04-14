import os
import requests
from flask import Flask, request
import openai

app = Flask(__name__)

# OpenAI credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ultramsg credentials
INSTANCE_ID = "instance114527"
TOKEN = "bo65xrcxtrw7jnxy"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    sender = data.get("from")
    message = data.get("body")

    if sender and message:
        # Get GPT response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي متخصص في العقارات في مصر. رد على العملاء بطريقة احترافية."},
                {"role": "user", "content": message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]

        # Send reply via Ultramsg
        requests.post(
            f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat",
            json={
                "to": sender,
                "body": reply,
                "priority": "10",
                "referenceId": ""
            },
            headers={"Content-Type": "application/json", "token": TOKEN}
        )

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
