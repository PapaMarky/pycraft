import os
import python_nbt.nbt as nbt
import glob

class Player:
    def __init__(self, world_path):
        flist = glob.glob(os.path.join(world_path, 'playerdata', '*.dat'))
        if len(flist) > 1:
            print('Too many players:')
            for f in flist:
                print(' - f')
                raise Exception('Too many players')

        self._path = flist[0]
        self._nbt_data = nbt.read_from_nbt_file(self._path)
    
    def get_attr_list(self):
        return list(self._nbt_data)

    def get_attr(self, name):
        if name in self._nbt_data:
            return self._nbt_data[name]

        
    @property
    def position(self):
        return self.get_attr('Pos').json_obj(full_json=False)
