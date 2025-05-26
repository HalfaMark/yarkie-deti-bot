import os
import traceback
import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        message_text = data['message']['text']
        chat_id = data['message']['chat']['id']

        if message_text.lower() == "/start":
            send_message(chat_id, "Привет! Я бот, задавай мне вопросы.")
            return jsonify({"ok": True})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты дружелюбный ассистент, который помогает родителям с вопросами о детских занятиях."},
                    {"role": "user", "content": message_text}
                ]
            )
            reply = response.choices[0].message.content.strip()
            reply = reply[:4000]  # Telegram limit
            send_message(chat_id, reply)

        except Exception as e:
            import traceback
            print("Full error:")
            traceback.print_exc()
            send_message(chat_id, "Что-то пошло не так. Мы уже чиним!")

    except Exception as e:
        import traceback
        traceback.print_exc()
        send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

    return jsonify({"ok": True})


@app.route('/')
def home():
    return 'Bot is running!'

if __name__ == '__main__':
    app.run(debug=False)
