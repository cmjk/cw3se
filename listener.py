import json
from telethon import TelegramClient, events

messages = []

cfg = json.load(open('config.json', 'r'))

api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']

client = TelegramClient('session', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start(phone=phone)


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/cwExchange')))
def my_event_handler(event):
    print(event.message)


client.idle()
