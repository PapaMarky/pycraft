import os

from math import floor
from pycraft import mca

# Notes: Region is 32x32 chunks or 512x512 blocks.
# chunks are 16x16 blocks

class Region:
    REGION_CACHE = {}

    def from_position_xy(world_path, x, y):
        '''
        Create a region from a world position
        '''
        rx = floor(x / 512.0)
        ry = floor(y / 512.0)
        return Region(world_path, rx, ry)

    def __init__(self, world_path, x, y):
        self._pos = [x, y]
        # filename for region, entities, and poi
        self._fname = f'r.{x}.{y}.mca'
        self._world_path = world_path
        self._data = {
            'poi': None,
            'entities': None,
            'region': None
        }
        
    def load_data(self, dtype):
        '''
        dtype is one of "region", "entities", or "poi"
        '''
        if dtype not in ('region', 'entities', 'poi'):
            raise Exception(f'Bad data type: {dtype}')

        if not self._data[dtype]:
            data_path = os.path.join(self._world_path, dtype, self._fname)
            self._data[dtype] = mca.Mca(data_path)
            
    def load_poi_data(self):
        self.load_region_data('poi')

    def load_entities_data(self):
        self.load_data('entities')

    def load_region_data(self):
        self.load_data('region')

