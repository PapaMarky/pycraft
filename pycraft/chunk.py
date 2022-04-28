import io
import json

from pycraft import nbt


class Chunk:
    BLOCK_WIDTH = 32

    def __init__(self, data, size):
        self._chunk_data = data
        self._tags = None
        self._size = size
        if self._chunk_data:
            byte_data = io.BytesIO(self._chunk_data)
            self._tags = nbt.read_bytes(byte_data).value

    def get_tags(self):
        return self._tags

    def as_json(self):
        if self._tags:
            return json.dumps(self._tags)
        return '{}'

    @property
    def size(self):
        return self._size

    @property
    def data_version(self):
        return self.get_tag('DataVersion')

    def get_tag(self, tag):
        if self._tags and tag in self._tags:
            return self._tags[tag]

    def get_tag_obj(self, tag):
        if self._tags and tag in self._tags:
            return self._tags[tag]

    def list_tags(self):
        if not self._tags:
            return None
        for tag in self._tags:
            print(tag)


class PoiSection:
    """
    Wrapper for Poi Chunk Section
    """

    def __init__(self, section):
        self._section = section

    def get_attribute(self, attribute_name: str):
        return self._section[attribute_name] if attribute_name in self._section else None

    def get_attribute_list(self):
        attribute_list = []
        for a in self._section:
            attribute_list.append(a)
        return attribute_list

    @property
    def records(self):
        return self.get_attribute('Records') or []


class PoiChunk(Chunk):
    def __init__(self, data, size):
        super().__init__(data, size)

    @property
    def sections(self):
        return self.get_tag('Sections') or {}


class EntitiesChunk(Chunk):
    def __init__(self, data, size):
        super().__init__(data, size)

    @property
    def entities(self):
        return self.get_tag('Entities') or {}

    def position(self):
        return self.get_tag('Position')


class RegionChunk(Chunk):
    def __init__(self, data, size):
        super().__init__(data, size)

    @property
    def status(self):
        return self.get_tag('Status')

    @property
    def position(self):
        x = self.get_tag('xPos')
        y = self.get_tag('yPos')
        z = self.get_tag('zPos')
        return x, y, z

    @property
    def structures(self):
        return self.get_tag('structures')

# Status x
# zPos x
# block_entities
# yPos x
# LastUpdate
# structures x
# InhabitedTime
# xPos x
# blending_data
# Heightmaps
# sections
# isLightOn
# block_ticks
# PostProcessing
# DataVersion
# fluid_ticks
