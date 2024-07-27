from sendRest import fetch_data
import requests
import time

# Konfigurasi bot Telegram
TOKEN = '7406952268:AAGTL34KcTAptBmLrCbL-8sJd-ZmdRaTQ70'
CHAT_ID = '7179689762'
MESSAGE = 'Terdapat kenakalan remaja, harap periksa aplikasi'

def send_telegram_message(token, chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    while True:
        # Ambil data dari Firebase
        mq3_data, mq135_data = fetch_data()

        # Gunakan data dalam aplikasi
        print(f"MQ3 Data from main.py: {mq3_data}")
        print(f"MQ135 Data from main.py: {mq135_data}")

        # Kirim pesan ke Telegram jika data valid
        if mq3_data and mq135_data:
            message = f"MQ3 Data: {mq3_data}\nMQ135 Data: {mq135_data}\nTerdapat kenakalan remaja, harap periksa aplikasi"
            send_telegram_message(TOKEN, CHAT_ID, message)
            print("Message sent to Telegram")
        else:
            print("No valid data to send")

        # Tunggu sebelum pengulangan berikutnya
        time.sleep(10)  # Mengirim pesan setiap 10 detik, sesuaikan dengan kebutuhan Anda

if __name__ == "__main__":
    main()
