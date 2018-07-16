import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd
import string


class ParsedMessage:
    def __init__(self, _id, timestamp):
        self._id = _id
        self.timestamp = timestamp

    def to_json(self):
        self.timestamp = self.timestamp.isoformat()
        return self.__dict__

    def to_string(self):
        return json.dumps(self.to_json())


class Transaction(ParsedMessage):
    def __init__(self, _id, timestamp, resource, quantity, price):
        super().__init__(_id, timestamp)
        self.resource = resource
        self.quantity = int(quantity)
        self.price = int(price)
        self.total = self.price * self.quantity


class Lot(ParsedMessage):
    def __init__(self, _id, timestamp, lot_id, item, price, buyer, status):
        super().__init__(_id, timestamp)
        self.lot_id = int(lot_id)
        while not item[0] in string.ascii_uppercase:
            item = item[1:]
        self.item = item.lower()
        self.price = int(price)
        self.buyer = buyer
        self.status = status

    def is_active(self):
        return self.status == '#active'

    def is_finished(self):
        return self.status == 'Finished'

    def has_bids(self):
        return self.buyer != 'None'


class AuctionHouse:
    def __init__(self, history):
        data = []
        with open(history, 'r') as f:
            for line in f:
                _ = json.loads(line)
                _['timestamp'] = datetime.datetime.strptime(_['timestamp'], '%Y-%m-%dT%H:%M:%S')
                data.append(_)
        self.df = pd.DataFrame.from_records(data)

    def structure(self):
        print(list(self.df))

    def last5trades(self, item):
        df = self.df[['price', 'timestamp']].where(self.df.item == item).sort_values(by=['timestamp'], ascending=False)
        print(df[['price']].head(n=5).values.tolist())

    def plot(self, item):
        self.df.where(self.df.item == item).plot(x='timestamp', y='price', label=item)
        plt.show()


class Message:
    def __init__(self, raw_msg):
        self._id = raw_msg.id
        self.date = raw_msg.date
        self.edit_date = raw_msg.edit_date
        self.msg = raw_msg.message

    def parse_transactions(self):
        resource = ''
        transactions = []

        for line in self.msg.splitlines():
            if line[0] in string.ascii_uppercase:
                resource = line[0:-1]
            else:
                q, p = line.split(',')[-1][1:-1].split(' x ')
                transactions.append(Transaction(self._id, self.date, resource, q, p))

        return transactions

    def parse_lot(self):
        if self.edit_date is not None:
            self.date = self.edit_date
        lines = self.msg.splitlines()
        lot_id = lines[0].split(' ')[1][1:]
        item = lines[0].split(' : ')[1]
        price = lines[2].split(' ')[2]
        buyer = lines[3].split(': ')[1]
        status = lines[5].split(': ')[1]
        return Lot(self._id, self.date, lot_id, item, price, buyer, status)
