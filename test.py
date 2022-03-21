#!/usr/bin/env python3

import json
import os
import sys

from pycraft import mca
from pycraft import Player
import python_nbt.nbt as nbt

WORLD_PATH = '/Users/mark/Library/Application Support/minecraft/saves/New World'

PLAYER_PATH = os.path.join(WORLD_PATH, 'playerdata/c36e8da7-f96b-46f2-a3f8-3171f22bcb95.dat')

if __name__ == '__main__':
    player = Player(WORLD_PATH)
    alist = player.get_attr_list()
    print(f'Position: {player.position}')
    sys.exit(0)
    for attr in alist:
        a = player.get_attr(attr)
        try:
            json_str = json.dumps(a.json_obj(full_json=False), indent=2)
            print(f'{attr}: {json_str}')
        except:
            print(f'{attr}: {a}')
        print('---')

