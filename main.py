import os
import openai
import requests
from flask import Flask, request

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты дружелюбный ассистент, который помогает родителям с вопросами о детских занятиях."},
            {"role": "user", "content": message_text}
        ]
    )
    reply = response.choices[0].message.content.strip()
    send_message(chat_id, reply)

except Exception as e:
    import traceback
    print("Full error:")
    traceback.print_exc()  # This will show real issue in Render logs
    send_message(chat_id, "Что-то пошло не так. Мы уже чиним!")


        send_message(chat_id, reply)

    return "ok"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
