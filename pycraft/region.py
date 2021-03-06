import os
from math import floor

from pycraft import mca
from pycraft.chunk import EntitiesChunk
from pycraft.chunk import PoiChunk
from pycraft.chunk import RegionChunk
from pycraft.error import PycraftException
from pycraft.mca_file import McaFile


# Notes: Region is 32x32 chunks or 512x512 blocks.
# chunks are 16x16 blocks

class Region(McaFile):
    REGION_CACHE = {}
    DATA_TYPES = ('region', 'entities', 'poi')

    BLOCK_WIDTH = 512

    @staticmethod
    def from_position_xy(world_path, x, y):
        """
        Create a region from a world position
        """
        rx = floor(x / Region.BLOCK_WIDTH)
        ry = floor(y / Region.BLOCK_WIDTH)
        return Region(world_path, rx, ry)

    def __init__(self, world_path, x, y):
        super().__init__()
        self._pos = [x, y]
        # filename for region, entities, and poi
        self._fname = f'r.{x}.{y}.mca'
        self._world_path = world_path
        self._data = {
            'poi': None,
            'entities': None,
            'region': None
        }

    def get_r_chunk(self, dtype, cx, cy):
        # convert world chunk to region chunk
        x = floor(cx) % 32
        y = floor(cy) % 32
        data = self.get_data(dtype)
        d = data.get_data(x, y)
        if data:
            size = data.get_data_size(x, y)
            chunk_class = {'poi': PoiChunk, 'entities': EntitiesChunk, 'region': RegionChunk}
            return chunk_class[dtype](d, size)
        return None

    def get_data(self, dtype):
        """
        Get the mca data file for dtype for this region.

        dtype is one of "region", "entities", or "poi"
        """
        if dtype not in ('region', 'entities', 'poi'):
            raise PycraftException(f'Bad data type: {dtype}')

        if not self._data[dtype]:
            data_path = os.path.join(self._world_path, dtype, self._fname)
            self._data[dtype] = mca.Mca(data_path)

        return self._data[dtype]

    @property
    def filename(self):
        return self._fname

    @property
    def pos(self):
        return self._pos
