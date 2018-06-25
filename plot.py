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

ax = df.where(df.resource == 'Pelt').plot(x='timestamp', y='price', label='Pelt')

for resource in ['Charcoal', 'Stick', 'Thread']:
    df.where(df.resource == resource).plot(x='timestamp', y='price', label=resource, ax=ax)

plt.show()
mean_price = df[['resource', 'price']].groupby('resource').agg('mean')
volume = df[['resource', 'quantity']].groupby('resource').agg('sum')

print(mean_price)
print(volume)
