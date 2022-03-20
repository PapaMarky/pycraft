from minecraft import chunk
from minecraft import error
from minecraft import mca

class McaFile:
    def __init__(self, path=None):
        self._path = path
        self._mca = None
        if self._path:
            self.load()

    def load(self):
        if not self._path:
            raise McExcpetion('McaFile: path not set')
        if not os.path.exists(self._path):
            raise McExcpetion(f'McaFile: file not found: "{self._path}"')
        self._mca = mca.Mca(self._path)
        
    def get_chunck(self, chunk_x, chunk_y):
        if not self._mca:
            raise McExcpetion('McaFile: Not open')
        return Chunk(self._mca.get_data(chunk_x, chunk_y)
