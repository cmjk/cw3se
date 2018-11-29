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

lots, active_lots = dict(), dict()


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/cwExchange')))
def transaction_new(event):
    with open('data.txt', 'a') as f:
        t = Message(event.message).parse_transactions()
        for tr in t:
            f.write(tr.to_string() + '\n')


@client.on(events.NewMessage(chats=client.get_entity('https://t.me/chatwars3')))
def lot_new(event):
    m = Message(event.message).parse_lot()
    with open('new_lots.txt', 'a') as f:
        f.write(m.to_string() + '\n')


@client.on(events.MessageEdited(chats=client.get_entity('https://t.me/chatwars3')))
def lot_edit(event):
    m = Message(event.message).parse_lot()
    if m.is_active():
        print('Price Updated: {}'.  format(m.lot_id))
    else:
        print('Finished: {}'.format(m.lot_id))
        with open('finished_lots.txt', 'a') as f:
            f.write(m.to_string() + '\n')


client.idle()
