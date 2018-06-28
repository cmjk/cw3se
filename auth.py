import json
from telethon import TelegramClient

messages = []

cfg = json.load(open('config.json', 'r'))

api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']

client = TelegramClient('session', api_id, api_hash)
client.start(phone=phone)


src = client.get_entity('https://t.me/chatwars3')
for item in client.iter_messages(src, min_id=32):
    messages.append(item.to_dict())

print(messages)
