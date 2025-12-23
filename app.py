"""
TradingView to Telegram Alert Server
Deploy su Render.com o Railway.app (GRATUITO)
"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Configurazione Telegram
TELEGRAM_BOT_TOKEN = "8056048982:AAHZYpPdPgqX6K-t_zuL2SI4xK-VWpeuvkE"
TELEGRAM_CHAT_ID = "5017851215"

def send_telegram(message):
    """Invia messaggio su Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Errore Telegram: {e}")
        return None

@app.route('/')
def home():
    """Pagina principale"""
    return """
    <html>
        <head>
            <title>TradingView Alert Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #667eea; }
                .status { 
                    background: #d4edda; 
                    padding: 15px; 
                    border-radius: 5px;
                    margin: 20px 0;
                    border-left: 4px solid #28a745;
                }
                .code {
                    background: #f8f9fa;
                    padding: 10px;
                    border-radius: 5px;
                    font-family: monospace;
                    overflow-x: auto;
                }
                .button {
                    background: #667eea;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Server Alert Attivo!</h1>
                <div class="status">
                    ✅ Il server è online e pronto a ricevere alert da TradingView
                </div>
                
                <h3>📡 URL Webhook</h3>
                <p>Usa questo URL in TradingView:</p>
                <div class="code" id="webhookUrl">Caricamento...</div>
                
                <h3>📝 Messaggio per TradingView</h3>
                <p>Nel campo "Message" dell'alert, inserisci:</p>
                <div class="code">
{
  "symbol": "{{ticker}}",
  "price": "{{close}}",
  "time": "{{timenow}}",
  "type": "{{plot_0}}"
}
                </div>
                
                <br>
                <button class="button" onclick="testWebhook()">🧪 Testa Connessione</button>
                <div id="testResult" style="margin-top: 10px;"></div>
            </div>
            
            <script>
                // Mostra URL del webhook
                document.getElementById('webhookUrl').textContent = 
                    window.location.origin + '/webhook';
                
                // Funzione test
                function testWebhook() {
                    const result = document.getElementById('testResult');
                    result.innerHTML = '<p>⏳ Invio messaggio di test...</p>';
                    
                    fetch('/test')
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                result.innerHTML = '<div class="status">✅ Test riuscito! Controlla Telegram</div>';
                            } else {
                                result.innerHTML = '<p style="colo
