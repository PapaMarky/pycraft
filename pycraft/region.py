import io
import os
import sys

from math import floor
from pycraft import mca
from pycraft import nbt
from pycraft.mca_file import McaFile
from pycraft.chunk import Chunk
from pycraft.chunk import PoiChunk
from pycraft.chunk import RegionChunk
from pycraft.chunk import EntitiesChunk

# Notes: Region is 32x32 chunks or 512x512 blocks.
# chunks are 16x16 blocks

class Region(McaFile):
    REGION_CACHE = {}
    DATA_TYPES = ('region', 'entities', 'poi')

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

    def get_chunk(self, dtype, cx, cy):
        ## convert world chunk to region chunk
        x = floor(cx)%32
        y = floor(cy)%32
        data = self.get_data(dtype)
        d = data.get_data(x, y)
        if d:
            bytedata = io.BytesIO(d)
            tags = nbt.read_bytes(bytedata)
        if data:
            chunk_class = {'poi': PoiChunk, 'entities': EntitiesChunk, 'region': RegionChunk}
            return chunk_class[dtype](d)
        return None

    def get_data(self, dtype):
        '''
        Get the mca data file for dtype for this region.

        dtype is one of "region", "entities", or "poi"
        '''
        if dtype not in ('region', 'entities', 'poi'):
            raise Exception(f'Bad data type: {dtype}')

        if not self._data[dtype]:
            data_path = os.path.join(self._world_path, dtype, self._fname)
            self._data[dtype] = mca.Mca(data_path)

        return self._data[dtype]
