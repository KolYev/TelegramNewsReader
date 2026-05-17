from telethon.sync import TelegramClient

import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = int(input("Введите api_id вашего аккаунта: "))
api_hash = str(input("Введите api_hash вашего аккаунта: "))
phone = str(input("Введите номер телефона, привязанный к вашему аккаунту: "))

client = TelegramClient(phone, api_id, api_hash)
client.start()