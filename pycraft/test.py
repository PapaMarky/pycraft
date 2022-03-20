from pycraft import DatFile
import json

f = DatFile('/Users/mark/Library/Application Support/minecraft/saves/New World/data/map_106.dat')
data = f.get_data()

print(f'#### data: {data}')

with open('map_106.json', 'w') as jfile:
    jfile.write(json.dumps(data['data'], indent=2))

