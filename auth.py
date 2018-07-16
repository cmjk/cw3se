from telethon import TelegramClient
from entities import *

messages = []

cfg = json.load(open('config.json', 'r'))

api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']

client = TelegramClient('session', api_id, api_hash)
client.start(phone=phone)


src = client.get_entity('https://t.me/chatwars3')

prices = []
count = 0


for message in client.iter_messages(src, search='hunter boots recipe'):
    m = Message(message).parse_lot()
    if m.is_finished():
        count += 1
        prices.append(m.price)
    if count == 10:
        break

print(prices)
