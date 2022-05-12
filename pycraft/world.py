from datetime import datetime
from pathlib import Path

from pycraft.level import Level
from pycraft.player import Player
from pycraft.region import Region
from pycraft.error import PycraftException
from pycraft.map import Map

import os


class World:

    @staticmethod
    def get_saved_worlds():
        save_world_list = []
        savepaths = (
            '%HOME%/Library/Application Support/minecraft/saves',
            '%APPDATA%.minecraft'
            '%HOME%.minecraft'
        )
        # plat = platform.system()
        home = str(Path.home())
        savedir = ''
        for path in savepaths:
            p = path.replace('%HOME%', home)
            if os.path.exists(p):
                savedir = p
                break

        _world_paths = {}
        for fname in os.listdir(savedir):
            _world_paths[fname] = os.path.join(savedir, fname)

        for world_name in _world_paths:
            world_path = _world_paths[world_name]
            print(f'path: {world_path}')
            level = Level(world_path)
            file_name = world_name
            icon_path = os.path.join(world_path, 'icon.png')
            name = level.LevelName
            last_played = level.LastPlayed
            # 0 is Survival, 1 is Creative, 2 is Adventure, 3 is Spectator
            mode_names = ['Survival', 'Creative', 'Adventure', 'Spectator']
            mode = mode_names[level.GameType]
            cheats = level.allowCommands
            dt = datetime.fromtimestamp(last_played/1000)
            version = level.Version['Name'].value
            save_world_list.append({
                'file_name': file_name,
                'icon_path': icon_path,
                'name': name,
                'last_played': dt,
                'mode': mode,
                'cheats': cheats,
                'version': version
            })
        save_world_list.sort(key=lambda x: x['last_played'], reverse=True)
        return save_world_list

    def __init__(self, path):
        self._path = path
        self._player = Player(path)
        self._level = Level(path)

    @property
    def level(self):
        return self._level

    @property
    def path(self):
        return self._path

    @property
    def map_path(self):
        """
        Return path of map file folder.

        Does not indicate the existence of maps
        """
        print(f'path: {self.path}')
        mp = os.path.join(self.path, 'data')
        return mp

    @staticmethod
    def _load_map(map_path):
        m = Map(map_path)
        return m

    def get_map(self, map_num):
        path = os.path.join(self.map_path, f'map_{map_num}.dat')
        return self._load_map(path)

    def get_region(self, pos):
        x, y = World.pos_to_xy(pos)
        return Region.from_position_xy(self._path, x, y)

    @staticmethod
    def block_to_chunk_pos(p):
        return int(p / 16)

    def get_chunk(self, pos, data_type):
        if data_type not in Region.DATA_TYPES:
            raise PycraftException(f'Bad data type: {data_type}')

        r = self.get_region(pos)
        _, y = World.pos_to_xy(pos)
        # convert world pos to chunk pos
        cx = self.block_to_chunk_pos(pos[0])
        cy = self.block_to_chunk_pos(pos[2])
        # print(f'--- CHUNK {cx}, {cy}')
        return r.get_r_chunk(data_type, cx, cy)

    @staticmethod
    def pos_to_xy(pos):
        if not isinstance(pos, list) and not isinstance(pos, tuple):
            print(f'type: {type(pos)}')
            raise PycraftException('pos is not a list')
        if len(pos) < 2 or len(pos) > 3:
            raise PycraftException('pos must be a list of 2 or 3 numbers')
        for v in pos:
            if not type(v) in (float, int):
                raise PycraftException('pos must be a list of 2 or 3 numbers')
        x = pos[0]
        y = pos[2] if len(pos) == 3 else pos[1]
        return x, y
