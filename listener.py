import logging
import json
import string
from telethon import TelegramClient, events

logging.basicConfig(level=logging.ERROR)

cfg = json.load(open('config.json', 'r'))
api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']


class Transaction:
    def __init__(self, timestamp, resource, quantity, price):
        self.timestamp = timestamp.strftime('"%d/%m/%y %H:%M"')
        self.resource = resource
        self.quantity = int(quantity)
        self.price = int(price)
        self.total = self.price * self.quantity


def message_parser(message):
    date = message.date
    msg = message.message
    resource = ''

    for line in msg.splitlines():
        if line[0] in string.ascii_uppercase:
            resource = line[0:-1]
        else:
            q, p = line.split(',')[-1][1:-1].split(' x ')
            print(json.dumps(Transaction(date, resource, q, p).__dict__))


client = TelegramClient('session', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start(phone=phone)


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/cwExchange')))
def my_event_handler(event):
    message_parser(event.message)


client.idle()
