from telethon.sync import TelegramClient

from datetime import datetime, timedelta, timezone

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = int(input("Введите api_id вашего аккаунта: "))
api_hash = str(input("Введите api_hash вашего аккаунта: "))
phone = str(input("Введите номер телефона, привязанный к вашему аккаунту: "))

# получаем текущее время
now = datetime.now(timezone.utc)

# сбрасываем время на начало дня
time_threshold = now.replace(hour=0, minute=0, second=0, microsecond=0)

with TelegramClient(phone, api_id, api_hash) as client:
    # Создаём файл для записи новостей за последний день
    with open("today_news.txt", "w", encoding="utf-8") as file:
        
        print("Получаем список каналов...")
        # Получаем все диалоги пользователя
        for dialog in client.get_dialogs():
            if dialog.is_channel:
                print(f"Сканирую канал: {dialog.name}")
                file.write(f"\n{'='*20} КАНАЛ: {dialog.name} {'='*20}\n\n")
                
                # Цикл сообщений от старых к новым
                for message in client.iter_messages(dialog):
                    # Если сообщение создано раньше чем вчера, то мы останавливаемся
                    if message.date < time_threshold:
                        break
                    
                    if message.text:
                        msg_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
                        file.write(f"[{msg_time}] {message.text}\n")
                        file.write("-" * 50 + "\n")