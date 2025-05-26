import os
import openai
import requests
from flask import Flask, request

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

system_prompt = {
    "role": "system",
    "content": "Ты — дружелюбный помощник детского сада 'Яркие Дети' из Ижевска. Отвечай кратко, по делу, и только по-русски. Если вопрос непонятный — предложи помощь администратора."
}

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        if not user_text:
            send_message(chat_id, "Пожалуйста, отправьте текстовое сообщение.")
            return "OK"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[system_prompt, {"role": "user", "content": user_text}],
                temperature=0.4,
                max_tokens=500
            )
            reply = response["choices"][0]["message"]["content"]
        except Exception as e:
            reply = "Произошла ошибка. Пожалуйста, попробуйте позже."

        send_message(chat_id, reply)

    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
