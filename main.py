from telethon.sync import TelegramClient

from datetime import datetime, timedelta, timezone

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from ai import Agent
from rich.console import Console

api_id = int(input("Введите api_id вашего аккаунта: "))
api_hash = str(input("Введите api_hash вашего аккаунта: "))
phone = str(input("Введите номер телефона, привязанный к вашему аккаунту: "))

# получаем текущее время
now = datetime.now(timezone.utc)

# сбрасываем время на начало дня
time_threshold = now.replace(hour=0, minute=0, second=0, microsecond=0)

with TelegramClient(phone, api_id, api_hash) as client:
    # Создаём файл для записи новостей за сегодняшний день
    with open("today_news.txt", "w", encoding="utf-8") as file:
        
        print("Получаем список каналов...")
        # Получаем все диалоги пользователя
        for dialog in client.get_dialogs():
            if dialog.is_channel and dialog.entity.broadcast:
                print(f"Сканирую канал: {dialog.name}")
                file.write(f"\n{'='*20} КАНАЛ: {dialog.name} {'='*20}\n\n")
                
                # Цикл сообщений от новых к старым
                for message in client.iter_messages(dialog):
                    # Если сообщение создано раньше начала сегодняшнего дня, останавливаемся
                    if message.date < time_threshold:
                        break
                    
                    if message.text:
                        msg_time = message.date.strftime('%Y-%m-%d %H:%M:%S')
                        file.write(f"[{msg_time}] {message.text}\n")
                        file.write("-" * 50 + "\n")
                        
console = Console()

try:
    with open("today_news.txt", "r", encoding="utf-8") as f:
        news_text = f.read()
        
    if not news_text.strip():
        console.print("[yellow]Нет новостей.[/yellow]")
        exit(0)
        
    prompt = (
        "Прочитай все новости, которые будут переданы ниже. "
        "Напиши краткое содержание прошедшего дня: основные темы, самые важные события, "
        "необычные происшествия. Уложись в 7-10 предложений. "
        "Отвечай на русском языке.\n\n"
        "=== НОВОСТИ ===\n"
        f"{news_text}\n"
        "=== КОНЕЦ НОВОСТЕЙ ==="
    )
    
    agent = Agent(model="qwen3.5-0.8b")
    
    with console.status("[dim]Thinking...[/dim]", spinner="arc"):
        response = agent.chat(prompt)
        
    console.print(f"[blue]Assistant: [/blue] {response}")
    
except FileNotFoundError:
    console.print("[red]Ошибка: файл today_news.txt не найден.[/red]")
except ConnectionError:
    console.print("[red]Ошибка: не удалось подключиться к локальному серверу ИИ.[/red]")
except Exception as e:
    console.print(f"[red]Произошла ошибка: {e}[/red]")