import time
import requests
from datetime import datetime
from python_telegram_bot import TelegramBot

# Configurazione Telegram
telegram_token = 'tuo_token'
telegram_chat_id = 'id_chat'  # ID della chat su Telegram dove inviare i messaggi
bot = TelegramBot(token=telegram_token)

# Coppie da monitorare
pairs = ['bitcoin', 'ethereum', 'solana']  # Simboli delle criptovalute su Coingecko

def get_volume(pair):
    try:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={pair}&vs_currencies=usd&include_24hr_vol=true'
        response = requests.get(url)
        data = response.json()
        
        if pair in data and 'usd' in data[pair]:
            volume = data[pair]['usd_24h_vol']
            return float(volume)
        else:
            print(f"Dati non trovati per {pair}")
            return None
    except Exception as e:
        print(f"Errore durante la richiesta API Coingecko: {e}")
        return None

def monitor_volume():
    while True:
        try:
            for pair in pairs:
                volume = get_volume(pair)
                if volume is None:
                    continue

                if volume > 0:  # Se il volume è maggiore di zero, consideriamo attivo il monitoraggio
                    message = f"📊 Volume in 24 ore di {pair.capitalize()}: ${volume:,.2f}"
                    bot.send_message(chat_id=telegram_chat_id, text=message)

            time.sleep(3600)  # Attendi un'ora prima di controllare di nuovo
        except Exception as e:
            print(f"Errore durante il monitoraggio: {e}")
            time.sleep(60)  # Attendi 1 minuto prima di riprovare

if __name__ == "__main__":
    monitor_volume()
