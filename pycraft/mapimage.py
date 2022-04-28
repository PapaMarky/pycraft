# Create an image from map.dat files
import json
import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pycraft.chunk import Chunk
from pycraft.chunk import PoiSection
from pycraft.colors import get_dye_color
from pycraft.error import PycraftException
from pycraft.region import Region
from pycraft.world import World


class MapImage:
    def __init__(self, config_file_path):
        self._config = None
        self.images = {}
        self.load_config(config_file_path)
        self.w0 = None
        self.w = 0
        self.h = 0
        self.block_w = None
        self.mapimage = None
        self.load_map_data()
        self.imgsize = None
        self.banner_font_size = int(5 * self.scale)
        self.banner_font = ImageFont.truetype('Keyboard.ttf', size=self.banner_font_size)
        self.mapobj = None
        self.maporigin = None
        self.mapsize = None
        self.world = None
        self.scale = 1
        self.map_background_color = '#000000'
        self.bannerW = 6
        self.bannerH = 8

    def create_image(self):
        self.stitch_maps()
        self.draw_map_borders()
        self.draw_region_borders()
        self.draw_village_borders()
        self.add_banners()

    def save_image(self, fname):
        print(f'Writing map to {fname}')
        if not self.mapimage:
            raise PycraftException(f'Map image not created. Call create_image() to create the map image')
        self.mapimage.save(fname)

    def stitch_maps(self):
        self.mapimage = Image.new(mode="RGBA", size=(self.w, self.h), color=self.map_background_color)
        self.imgsize = (self.mapimage.width, self.mapimage.height)
        dy = 0
        for row in self._config['map']:
            dx = 0
            for m in row:
                self.mapimage.paste(self.images[m], (int(dx), int(dy)), self.images[m])
                dx += self.w0
            dy += self.w0

    def block_to_map(self, pos):
        ox = self.maporigin[0]
        oz = self.maporigin[1]
        x = pos[0]
        y = pos[2] if len(pos) > 2 else pos[1]

        x_pct = (x - ox) / self.mapsize[0]
        y_pct = (y - oz) / self.mapsize[1]
        pix_x = int(x_pct * self.imgsize[0])
        pix_y = int(y_pct * self.imgsize[1])
        return pix_x, pix_y

    def draw_banner(self, banner):
        pos = banner['pos']
        color = banner['color']
        name = banner['name']
        pix_x, pix_y = self.block_to_map(pos)
        banner_x = int(self.bannerW / 2)
        banner_y = int(self.bannerH / 3)
        poly_pts = (
            (pix_x, pix_y),
            (pix_x + banner_x, pix_y - banner_y),
            (pix_x + banner_x, pix_y - self.bannerH),
            (pix_x - banner_x, pix_y - self.bannerH),
            (pix_x - banner_x, pix_y - banner_y)
        )
        banner_color = get_dye_color(color)
        draw = ImageDraw.Draw(self.mapimage)
        draw.polygon(poly_pts, fill=banner_color, outline='black')

        if name:
            draw.text((pix_x - 1, pix_y - 1), name, fill='black', anchor='ma', font=self.banner_font)
            draw.text((pix_x + 1, pix_y + 1), name, fill='black', anchor='ma', font=self.banner_font)
            draw.text((pix_x, pix_y), name, fill='white', anchor='ma', font=self.banner_font)

    def add_banners(self):
        print(f'Adding banners...')
        dx = 0
        dy = 0

        # TODO : font_size should come from config
        self.banner_font_size = int(5 * self.scale)
        # TODO : config should contain a list of "banner fonts" and try each until successful
        for row in self._config['map']:
            for m in row:
                mapobj = self.world.get_map(m)
                banners = mapobj.get_banners()
                for banner in banners:
                    self.draw_banner(banner)
                dx += self.w0
            dy += self.w0

    def load_map_data(self):
        row_num = 0
        for row in self._config['map']:
            print(f'--row {row_num}--')
            row_num += 1
            for m in row:
                self.mapobj = self.world.get_map(m)
                print(f'-- map {m} Center: {self.mapobj.get_center()} Origin: {self.mapobj.get_origin()} --')
                if self.w0 is None:
                    self.w0 = self.mapobj.get_width() * self.scale
                    self.w = int(len(self._config['map'][0]) * self.w0)
                    self.h = int(len(self._config['map']) * self.w0)
                    self.block_w = self.mapobj.width_in_blocks()
                img = self.mapobj.create_image(scale=self.scale)
                if 'saveall' in self._config and self._config['saveall']:
                    print(f'Saving map image: map_{m}.png')
                    img.save(f'map_{m}.png')
                self.images[m] = img

        map_0_0 = self.world.get_map(self._config['map'][0][0])
        self.maporigin = map_0_0.get_origin()
        self.mapsize = (len(self._config['map'][0]) * self.block_w, len(self._config['map']) * self.block_w)

    def load_config(self, config_file):
        with open(config_file) as cfile:
            self._config = json.loads(cfile.read())
        self.world = World(self._config['path'])
        self.scale = self._config['scale'] if 'scale' in self._config else 1.0
        print(f'Scale: {self.scale}')
        # select 102, 76, 51 as background color to mimic maps in a frame
        self.map_background_color = self._config[
            'background_color'] if 'background_color' in self._config else '#835432'

    def draw_map_borders(self):
        if not self._config['map_borders']:
            return
        nmaps = (len(self._config['map'][0]), len(self._config['map']))
        clr = self._config['map_borders']
        line_w = 2
        draw = ImageDraw.Draw(self.mapimage)

        xstep = int(self.mapimage.width / nmaps[0])
        x = 0
        while x < self.mapimage.width:
            draw.line([(x, 0), (x, self.mapsize[1])], fill=clr, width=line_w)
            x += xstep

        ystep = int(self.mapimage.height / nmaps[1])
        y = 0
        while y < self.mapimage.height:
            draw.line([(0, y), (self.mapsize[0], y)], fill=clr, width=line_w)
            y += ystep

    def draw_region_borders(self):
        if not self._config['region_borders']:
            return
        clr = self._config['region_borders']
        line_w = 3
        draw = ImageDraw.Draw(self.mapimage)

        x0 = int(math.floor(self.maporigin[0] / Region.BLOCK_WIDTH) * Region.BLOCK_WIDTH)
        y0 = int(math.floor(self.maporigin[1] / Region.BLOCK_WIDTH) * Region.BLOCK_WIDTH)
        print(f'Region Origin: ({x0}, {y0})')
        xstep = ystep = Region.BLOCK_WIDTH
        x = x0
        while x < self.mapsize[0]:
            if x >= self.maporigin[0]:
                p0 = self.block_to_map((x, 0, y0))
                p1 = self.block_to_map((x, 0, self.mapsize[1]))
                draw.line([p0, p1], fill=clr, width=line_w)
            x += xstep
        y = y0
        while y < self.mapsize[1]:
            if y >= self.maporigin[1]:
                p0 = self.block_to_map((x0, 0, y))
                p1 = self.block_to_map((self.mapsize[0], 0, y))
                draw.line([p0, p1], fill=clr, width=line_w)
            y += ystep

    def draw_village_borders(self):
        if not self._config['villages']:
            return
        # load bells from all regions on map
        start_pos = self.maporigin
        last_map = self.world.get_map(self._config['map'][-1:][0][-1:][0])
        o = last_map.get_origin()
        bw = last_map.width_in_blocks()
        end_pos = (o[0] + bw, o[1] + bw)
        vcenters = []
        # visit each region on map collecting bells
        print(f'Start: {start_pos}, End: {end_pos}')
        print(f' - This will take a long time...')
        y = start_pos[1]
        while y < end_pos[1] + Region.BLOCK_WIDTH:
            x = start_pos[0]
            while x < end_pos[0] + Region.BLOCK_WIDTH:
                region = self.world.get_region((x, 0, y))
                # print(f'Region of ({x}, {Y}): {region.filename}')
                for cy in range(Chunk.BLOCK_WIDTH):
                    for cx in range(Chunk.BLOCK_WIDTH):
                        try:
                            chunk = region.get_r_chunk('poi', cx, cy)
                        except PycraftException:
                            # region doesn't exist
                            continue
                        sections = chunk.sections
                        for section in sections:
                            s = PoiSection(sections[section])
                            records = s.records
                            for record in records:
                                t = record['type'].value
                                if t.startswith('minecraft:'):
                                    t = t[10:]
                                if t == 'meeting':
                                    pos = record['pos'].value
                                    tickets = record['free_tickets'].value
                                    vcenters.append({'pos': pos, 'tickets': tickets})
                x += Region.BLOCK_WIDTH
            y += Region.BLOCK_WIDTH
        print(f'FOUND {len(vcenters)} villages')
        # Now draw boxes around all the villages
        draw = ImageDraw.Draw(self.mapimage)
        village_w = 32  # village width
        for village in vcenters:
            pos = village['pos']
            p0 = self.block_to_map((pos[0] - village_w, pos[2] - village_w))
            p1 = self.block_to_map((pos[0] + village_w, pos[2] + village_w))
            draw.rectangle((p0, p1), outline=self._config['villages'], width=1)
