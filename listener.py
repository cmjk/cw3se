import logging
from telethon import TelegramClient, events
from entities import *
logging.basicConfig(level=logging.ERROR)

cfg = json.load(open('config.json', 'r'))
api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']

client = TelegramClient('session', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start(phone=phone)


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/cwExchange')))
def transaction(event):
    with open('data2.txt', 'a') as f:
        f.write(Message(event.message).parse_transaction().to_string() + '\n')


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/chatwars3')))
def new_lot(event):
    with open('lots.txt', 'a') as f:
        f.write(Message(event.message).parse_lot().to_string() + '\n')


client.idle()
