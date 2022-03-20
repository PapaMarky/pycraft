from minecraft import DatFile
import json

f = DatFile('/Users/mark/Library/Application Support/minecraft/saves/New World/data/map_106.dat')
data = f.get_data()
# print(f'DATA: {data}')

with open('map_106.json', 'w') as jfile:
    jfile.write(json.dumps(data.json_obj(full_json=True), indent=2))

