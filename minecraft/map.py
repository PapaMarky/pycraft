
from minecraft.dat_file import DatFile
from minecraft.colors import colors as color_map
import json
import sys
from PIL import Image

# info about map scaling:
# https://minecraft.fandom.com/wiki/Map#Zoom_details

class Map(DatFile):
    def __init__(self, path):
        super().__init__(path)
        self._banners = None

    def get_origin(self):
        '''
        return the map origin (x, z) in world (block) coordinates
        '''
        c = self.get_center()
        bw = self.width_in_blocks()
        return (c[0] - (bw / 2.0), c[1] - (bw / 2.0))

    def get_zoom(self):
        return self._tags['data']['scale'].value

    def width_in_blocks(self):
        return (128, 256, 512, 1024, 2048)[self.get_zoom()]

    def get_banners(self):
        if self._banners is None:
            self._banners = []
            bdata = self._tags['data']['banners'].json_obj(full_json=False)
            for b in bdata:
                banner = {
                    'pos': (b['Pos']['X'], b['Pos']['Y'], b['Pos']['Z']), 
                    'color': b['Color'], 
                    'name': ''}
                if 'Name' in b:
                    banner['name'] = json.loads(b['Name'])['text']
                
                self._banners.append(banner)

        return self._banners

    def get_center(self):
        cx = self._tags['data']['xCenter'].value
        cz = self._tags['data']['zCenter'].value
        return (cx, cz)

    def block_to_pixel(self, coords):
        center = self.get_center()
    
    def get_colors(self):
        return self._tags['data']['colors']

    def get_width(self):
        colors = self.get_colors()
        lencolors = len(colors)
        width = 128 if lencolors == 16384 else math.sqrt(lencolors)
        return width
        
    def create_image(self, scale=1.0):
        width = self.get_width()
        img = Image.new(mode="RGBA", size=(width, width))
        print(f'WIDTH: {width}')
        print(f' ZOOM: {self.get_zoom()}')
        colors = self.get_colors()
        for y in range(width):
            for x in range(width):
                offset = x + y * width
                color_index = colors[offset]
                if color_index == 0:
                    color_index = 104
                if color_index < 0:
                    color_index = 256 + color_index
                if color_index >= len(color_map):
                    print(f'BAD VALUE: {color_index}: ({x}, {y}) x {width}: OFFSET: {offset}')
                    color_index = 75
                if color_index >= 48 and color_index <= 51:
                    color_index += 4
                try:
                    val = color_map[color_index]
                    img.putpixel((x,y), val)
                except Exception as ex:
                    print(f'Exception: {ex}')
                    print(f' - ({x}, {y}) = {offset}')
                    sys.exit(1)

        if scale != 1.0:
            img = img.resize((int(width * scale), int(width * scale)))

        return img
