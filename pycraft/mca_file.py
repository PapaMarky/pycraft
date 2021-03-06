import os

from pycraft.chunk import Chunk
from pycraft import mca
from pycraft.error import PycraftException


class McaFile:
    def __init__(self, path=None):
        self._path = path
        self._mca = None
        if self._path:
            self.load()

    def load(self):
        if not self._path:
            raise PycraftException('McaFile: path not set')
        if not os.path.exists(self._path):
            raise PycraftException(f'McaFile: file not found: "{self._path}"')
        self._mca = mca.Mca(self._path)

    def get_chunk_size(self, chunk_x, chunk_y):
        if not self._mca:
            raise PycraftException('McaFile: Not open')
        return self._mca.get_data_size(chunk_x, chunk_y)

    def get_chunk(self, chunk_x, chunk_y):
        if not self._mca:
            raise PycraftException('McaFile: Not open')
        return Chunk(self._mca.get_data(chunk_x, chunk_y), self._mca.get_data_size(chunk_x, chunk_y))
