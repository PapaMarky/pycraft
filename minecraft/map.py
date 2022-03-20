
from minecraft.dat_file import DatFile
from minecraft.colors import colors as color_map
from minecraft.colors import get_color
import json
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

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
        
    def create_image(self, scale=1.0, banners=True):
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
        if banners:
            zoom = self.get_zoom()
            center = self.get_center()
            bpp = (1, 2, 4, 8, 16)[zoom]/ scale
            map_origin = self.get_origin()
            blocks_wide = self.width_in_blocks()
            image_size = img.width
            #font = ImageFont.truetype("Tests/fonts/NotoSans-Regular.ttf", 48)
            font = ImageFont.truetype('Keyboard.ttf')
            def draw_banner(pos, color, name, img):
                ox = center[0] - (blocks_wide/2)
                oz = center[1] - (blocks_wide/2)
                print(f' map center: {center}')
                print(f'     origin: ({ox}, {oz})')
                print(f'        pos: ({pos[0]}, {pos[2]})')
                print(f' COLOR: "{color}"')
                x_pct = (pos[0] - ox) / blocks_wide
                y_pct = (pos[2] - oz) / blocks_wide
                print(f'offset: ({x_pct}, {y_pct})')
                pix_x = int(x_pct * image_size)
                pix_y = int(y_pct * image_size)
                print(f'img size: {image_size}')
                print(f'img pos: ({pix_x}, {pix_y})')
                poly_pts = (
                    (pix_x, pix_y),
                    (pix_x + 3, pix_y - 3),
                    (pix_x + 3, pix_y - 8),
                    (pix_x - 3, pix_y - 8),
                    (pix_x - 3, pix_y - 3)
                )
                banner_color = get_color(color)
                print(f'BANNER COLOR: {banner_color}')
                draw = ImageDraw.Draw(img)
                draw.polygon(poly_pts, fill=banner_color, outline='black')

                if name:
                    draw.text((pix_x-1, pix_y-1), name, fill='black', anchor='ma', font=font)
                    draw.text((pix_x+1, pix_y+1), name, fill='black', anchor='ma', font=font)
                    draw.text((pix_x, pix_y), name, fill='white', anchor='ma', font=font)

            banner_data = self.get_banners()
            if len(banner_data) > 0:
                print(f'BANNERS:')
                for b in banner_data:
                    draw_banner(b['pos'], b['color'], b['name'], img)
        return img
