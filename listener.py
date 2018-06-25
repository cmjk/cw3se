import logging
import json
import string
from telethon import TelegramClient, events

logging.basicConfig(level=logging.ERROR)

cfg = json.load(open('config.json', 'r'))
api_id = cfg['api_id']
api_hash = cfg['api_hash']
phone = cfg['phone']


class ParsedMessage:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def to_json(self):
        self.timestamp = self.timestamp.isoformat()
        return self.__dict__

    def to_string(self):
        return json.dumps(self.to_json())


class Transaction(ParsedMessage):
    def __init__(self, timestamp, resource, quantity, price):
        super().__init__(timestamp)
        self.resource = resource
        self.quantity = int(quantity)
        self.price = int(price)
        self.total = self.price * self.quantity


class Lot(ParsedMessage):
    def __init__(self, timestamp, item, price, status):
        super().__init__(timestamp)
        self.item = item
        self.price = price
        self.status = status

    def is_active(self):
        return self.status == '#active'


class Message:
    def __init__(self, raw_msg):
        self.date = raw_msg.date
        self.msg = raw_msg.message

    def parse_transaction(self):
        resource = ''

        for line in self.msg.splitlines():
            if line[0] in string.ascii_uppercase:
                resource = line[0:-1]
            else:
                q, p = line.split(',')[-1][1:-1].split(' x ')
                return Transaction(self.date, resource, q, p)

    def parse_lot(self):
        lines = self.msg.splitlines()
        item = lines[1].split(' : ')[1]
        price = lines[2].split(' ')[2]
        status = lines[5].split(': ')[1]
        return Lot(self.date, item, price, status)


client = TelegramClient('session', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start(phone=phone)


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/cwExchange')))
def my_event_handler(event):
    with open('data2.txt', 'a') as f:
        f.write(json.dumps(Message(event.message).parse_transaction().to_json()) + '\n')


client.idle()
