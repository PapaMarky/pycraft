from pycraft.player import Player
from pycraft.region import Region
from pycraft.chunk import Chunk
from pycraft.error import PycraftException
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
        x, y = World.pos_to_xy(pos)
        return Region.from_position_xy(self._path, x, y)

    def get_chunk(self, pos, data_type):
        if not data_type in Region.DATA_TYPES:
            raise PycraftException(f'Bad data type: {data_type}')

        r = self.get_region(pos)
        x, y = World.pos_to_xy(pos)
        # convert world pos to chunk pos
        cx = int(pos[0]/16)
        cy = int(pos[2]/16)
        return r.get_chunk(data_type, cx, cy)

    def pos_to_xy(pos):
        if not isinstance(pos, list) and not isinstance(pos, tuple):
            print (f'type: {type(pos)}')
            raise PycraftException('pos is not a list')
        if len(pos) < 2 or len(pos) > 3:
            raise PycraftException('pos must be a list of 2 or 3 numbers')
        for v in pos:
            if not type(v) in (float, int):
                raise PycraftException('pos must be a list of 2 or 3 numbers')
        x = pos[0]
        y = pos[2] if len(pos) == 3 else p[1]
        return x, y
