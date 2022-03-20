from pycraft.player import Player
from pycraft.error import PycraftExcpetion
from pycraft.map import Map

import os

class World:
    def __init__(self, path):
        self._path = path
        self._player = Player(path)

    def get_map(self, map_num):
        path = os.path.join(self._path, 'data', f'map_{map_num}.dat')
        m = Map(path)
        return m

    def get_region(self, pos):
        if not isinstance(pos, list) and not isinstance(pos, tuple):
            print (f'type: {type(pos)}')
            raise PycraftExcpetion('pos is not a list')
        if len(pos) < 2 or len(pos) > 3:
            raise PycraftExcpetion('pos must be a list of 2 or 3 numbers')
        for v in pos:
            if not type(v) in (float, int):
                raise PycraftExcpetion('pos must be a list of 2 or 3 numbers')
