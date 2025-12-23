from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8056048982:AAHZYpPdPgqX6K-t_zuL2SI4xK-VWpeuvkE"
TELEGRAM_CHAT_ID = "5017851215"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        return requests.post(url, json=data).json()
    except:
        return None

@app.route('/')
def home():
    return '<h1>Server Attivo</h1>'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or {}
    msg = f"Alert: {data.get('symbol', 'N/A')} - {data.get('price', 'N/A')}"
    send_telegram(msg)
    return jsonify({"ok": True})

@app.route('/test')
def test():
    send_telegram("Test OK")
    return '<h1>Test inviato</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
