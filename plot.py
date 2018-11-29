import matplotlib.pyplot as plt
import pandas as pd
import json
import datetime


raw_data2 = []


with open('data.txt', 'r') as f:
    for line in f:
        _ = json.loads(line)
        _['timestamp'] = datetime.datetime.strptime(_['timestamp'], '%Y-%m-%dT%H:%M:%S')
        raw_data2.append(_)

resources = set()
for item in raw_data2:
    resources.add(item['resource'])

df = pd.DataFrame.from_records(raw_data2)

_ = 'Vial of Rage'
# ax = df.where(df.resource == _).plot('timestamp', 'price', label=_, marker='o')

# for resource in ['Pelt']:
#    df.where(df.resource == resource).plot(x='timestamp', y='price', label=resource, ax=ax)

# plt.show()

volume = df[['resource', 'quantity', 'total']].groupby('resource').agg('sum')
volume['avg price'] = volume.total / volume.quantity
volume.rename({'total': 'volume'}, axis='columns', inplace=True)

r = 'Stick'
print('\n# of {} sold at pricepoint'.format(r))
print(df.where(df.resource == r).groupby('price').agg('sum').quantity)

print('\nTop 10 traded commodities')
print(volume.sort_values(by=['volume'], ascending=False).head(10))

potions = volume.filter(regex='Vial|Potion|Bottle', axis=0)
print('\nPotions')
print(potions)
print('\nTotal potions volume: ', potions['volume'].agg('sum'))
