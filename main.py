from telethon.sync import TelegramClient

import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = int(input("Введите api_id вашего аккаунта: "))
api_hash = str(input("Введите api_hash вашего аккаунта: "))
phone = str(input("Введите номер телефона, привязанный к вашему аккаунту: "))

client = TelegramClient(phone, api_id, api_hash)
client.start()

chats = []
last_date = None
size_chats = 200
groups=[]

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
        ))
chats.extend(result.chats)

for chat in chats:
   try:
       if chat.megagroup== True:
           groups.append(chat)
   except:
       continue
   
print('Список каналов:')
i=0
for g in groups:
   print(str(i) + '- ' + g.title)
   i+=1