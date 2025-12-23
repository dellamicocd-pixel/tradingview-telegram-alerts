from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8056048982:AAHZYpPdPgqX6K-t_zuL2SI4xK-VWpeuvkE"
TELEGRAM_CHAT_ID = "5017851215"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Errore: {e}")
        return None

@app.route('/')
def home():
    return f'''
    <h1>Server Attivo!</h1>
    <p>URL Webhook: {request.url_root}webhook</p>
    <a href="/test">Testa connessione</a>
    '''

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json() or {}
        
        symbol = data.get('symbol', 'N/A')
        price = data.get('price', 'N/A')
        signal_type = data.get('type', 'SIGNAL')
        time = data.get('time', datetime.now().strftime('%H:%M:%S'))
        
        message = f"🚨 ALERT TRADING\n\n💱 Simbolo: {symbol}\n📊 Tipo: {signal_type}\n💰 Prezzo: {price}\n⏰ Ora: {time}"
        
        send_telegram(message)
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/test')
def test():
    message = f"✅ Test riuscito!\n\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    result = send_telegram(message)
    
    if result and result.get('ok'):
        return "<h1>✅ Test riuscito! Controlla Telegram</h1>"
    else:
        return "<h1>❌ Errore</h1>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
