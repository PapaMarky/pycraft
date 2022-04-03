import python_nbt.nbt as nbt
import ctypes
import json

def EntityFactory(entity):
    if 'id' in entity and entity['id'].value in etypes:
        return etypes[entity['id'].value](entity)
    return Entity(entity)

class Entity():
    '''
    Wrapper for Entity

    Tags Info: https://www.digminecraft.com/data_tags/index.php
    '''
    def _make_uuid(uuid):
        out = []
        for d in uuid:
            d = ctypes.c_uint(int(d)).value
            out.append(d)
        return f'{out[0]:x}{out[1]:x}{out[2]:x}{out[3]:x}'
        
    def __init__(self, entity):
        self._entity = entity

    def is_type(self, ent_type):
        return self.id == ent_type

    def get_attribute(self, attrname):
        return self._entity[attrname] if attrname in self._entity else None

    def get_attribute_list(self):
        alist = []
        for a in self._entity:
            alist.append(a)
        return alist

    @property
    def brain(self):
        return self.get_attribute('Brain')

    @property
    def memories(self):
        b = self.brain
        if b and 'memories' in b:
            return b['memories'].value
        return None

    @property
    def owner(self):
        m = self.memories
        if m and 'Owner' in m:
            return m['Owner']
        return None

    @property
    def id(self):
        if 'id' in self._entity:
            v = self._entity['id'].value
            if v.startswith('minecraft:'):
                v = v[10:]
            return v
        return None

    @property
    def uuid(self):
        if 'UUID' in self._entity:
            return Entity._make_uuid(self._entity['UUID'])
        return None

    @property
    def position(self):
        p = self.get_attribute('Pos')
        if p:
            rval = []
            for v in p:
                rval.append(v.value)
            return rval
        return None
        
    @property
    def in_love(self):
        return self.get_attribute('InLove')

    @property
    def leash(self):
        return self.get_attribute('Leash')

    @property
    def chest(self):
        chested = self.get_attribute('ChestedHorse')
        return self.get_attribute('Items') if chested else None

    @property
    def color(self):

        '''
        see also colors.get_sheep_color()
        '''
        return self.get_attribute('Color')

    @property
    def custom_name(self):
        return self.get_attribute('CustomName')

    @property
    def passengers(self):
        return self.get_attribute('Passengers')

    @property
    def owner(self):
        if 'Owner' in self._entity:
            return Entity._make_uuid(self._entity['Owner'].value)
        return None

class PetEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)

class CatEntity(PetEntity):
    def __init__(self, entity):
        super().__init__(entity)

class DonkeyEntity(PetEntity):
    def __init__(self, entity):
        super().__init__(entity)
    
class VillagerEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)

    def get_memory(self, memory):
        m = self.memories
        mstr = f'minecraft:{memory}'
        if m and mstr in m:
            return  m[mstr]['value']
            
    @property
    def home(self):
        home = self.get_memory('home')
        
        if home:
            return {
                'pos': home.value['pos'].value,
                'dimension': home.value['dimension'].value
            }
        return None

    @property
    def meeting_point(self):
        mp = self.get_memory('meeting_point')
        if mp:
            return {
                'pos': mp.value['pos'].value,
                'dimension': mp.value['dimension'].value
            }
        return None

    @property
    def villager_data(self):
        if 'VillagerData' in self._entity:
            return self._entity['VillagerData']
        return None

    @property
    def profession(self):
        vd = self.villager_data
        if vd:
            return vd['profession'].value

etypes = {
    'minecraft:villager': VillagerEntity
    #'minecraft:cat': CatEntity,
    #'minecraft:donkey': DonkeyEntity
}
