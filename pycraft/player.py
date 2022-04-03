import os
import python_nbt.nbt as nbt
import glob

from math import floor

from pycraft.error import PycraftException
from pycraft.region import Region

class Player:
    def __init__(self, world_path):
        if not os.path.exists(world_path):
            print(f'Saved world not found: "{world_path}"')
            raise PycraftException('World not found')
        flist = glob.glob(os.path.join(world_path, 'playerdata', '*.dat'))
        if len(flist) < 1:
            print('No players found')
            raise PycraftException('Not enough players')
        if len(flist) > 1:
            print('Too many players:')
            for f in flist:
                print(f' - {f}')
            raise PycraftException('Too many players')

        uuid = ''.join(os.path.basename(flist[0])[:-4].split('-'))
        self._uuid = uuid
        self._path = flist[0]
        self._nbt_data = nbt.read_from_nbt_file(self._path)
        self._world_path = world_path
        self._region = None

    def get_attr_list(self):
        return list(self._nbt_data)

    def get_attr(self, name):
        if name in self._nbt_data:
            return self._nbt_data[name]

    def get_region(self):
        if self._region:
            return self._region

        p = self.position
        self._region = Region.from_position_xy(self._world_path, p[0], p[2])
        return self._region

    def get_vehicle(self):
        v = self.get_attr('RootVehicle')
        return v

    @property
    def chunk_position(self):
        p = self.position
        return (int(p[0]/16), int(p[1]/16), int(p[2]/16))

    @property
    def position(self):
        return self.get_attr('Pos').json_obj(full_json=False)

    @property
    def uuid(self):
        return self._uuid
