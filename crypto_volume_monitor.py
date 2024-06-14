import time
from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta
from python_telegram_bot import TelegramBot

# Configurazione API Binance
api_key = 'tuo_api_key'
api_secret = 'tuo_api_secret'
client = Client(api_key, api_secret)

# Configurazione Telegram
telegram_token = 'tuo_token'
telegram_chat_id = 'id_chat'  # ID della chat su Telegram dove inviare i messaggi
bot = TelegramBot(token=telegram_token)

# Coppie da monitorare e media del volume delle 15 candele precedenti
pairs = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
interval = '1h'
candles_limit = 16  # 15 + 1 (per ottenere le ultime 16 candele)

def get_volume_avg(pair):
    try:
        candles = client.get_klines(symbol=pair, interval=interval, limit=candles_limit)
        volumes = [float(candle[5]) for candle in candles[:-1]]  # Prendi solo i volumi delle prime 15 candele
        volume_avg = sum(volumes) / len(volumes)
        return volume_avg
    except BinanceAPIException as e:
        print(f"Errore API Binance: {e}")
        return None

def monitor_volume():
    while True:
        try:
            for pair in pairs:
                volume_avg = get_volume_avg(pair)
                if volume_avg is None:
                    continue

                current_candle = client.get_klines(symbol=pair, interval=interval, limit=1)[0]
                current_volume = float(current_candle[5])
                if current_volume >= 2 * volume_avg:
                    close_price = float(current_candle[4])
                    open_price = float(current_candle[1])
                    if close_price > open_price:
                        message = f"📈 High buying volume detected on {pair}! Volume: {current_volume}"
                    else:
                        message = f"📉 High selling volume detected on {pair}! Volume: {current_volume}"

                    # Invia messaggio su Telegram
                    bot.send_message(chat_id=telegram_chat_id, text=message)

            time.sleep(3600)  # Attendi un'ora prima di controllare di nuovo
        except Exception as e:
            print(f"Errore durante il monitoraggio: {e}")
            time.sleep(60)  # Attendi 1 minuto prima di riprovare

if __name__ == "__main__":
    monitor_volume()
