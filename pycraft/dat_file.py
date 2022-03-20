import python_nbt.nbt as nbt

class DatFile:
    def __init__(self, path):
        self._path = path
        self._tags = nbt.read_from_nbt_file(path)
        
    def get_data(self):
        return self._tags['data']
