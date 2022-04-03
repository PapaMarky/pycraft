## Create an image from map.dat files
from pycraft import World
from pycraft.colors import get_dye_color
from pycraft.error import PycraftException

import json
import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

class MapImage:
    def __init__(self, config_file_path):
        self._config = None
        self.images = {}
        self.load_config(config_file_path)
        self.w0 = None
        self.block_w = None
        self.mapimage = None
        self.load_map_data()

    def create_image(self):
        self.stitch_maps()
        self.add_banners()
        self.draw_region_borders()
        self.draw_map_borders()

    def save_image(self, fname):
        print(f'Writing map to {fname}')
        if not self.mapimage:
            raise PycraftException(f'Map image not created. Call create_image() to create the map image')
        self.mapimage.save(fname)

    def stitch_maps(self):
        dx = 0
        dy = 0
        self.mapimage = Image.new(mode="RGBA", size=(self.w, self.h), color=self.map_background_color)
        self.imgsize = (self.mapimage.width, self.mapimage.height)
        for row in self._config['map']:
            dx = 0
            for m in row:
                self.mapimage.paste(self.images[m], (int(dx), int(dy)), self.images[m])
                dx += self.w0
            dy += self.w0

    def block_to_map(self, pos):
        ox = self.maporigin[0]
        oz = self.maporigin[1]
        x_pct = (pos[0] - ox) / self.mapsize[0]
        y_pct = (pos[2] - oz) / self.mapsize[1]
        pix_x = int(x_pct * self.imgsize[0])
        pix_y = int(y_pct * self.imgsize[1])
        return pix_x, pix_y

    def draw_banner(self, banner):
        pos = banner['pos']
        color = banner['color']
        name = banner['name']
        pix_x, pix_y = self.block_to_map(pos)
        BX = int(self.bannerW/2)
        BY0 = int(self.bannerH/3)
        poly_pts = (
            (pix_x, pix_y),
            (pix_x + BX, pix_y - BY0),
            (pix_x + BX, pix_y - self.bannerH),
            (pix_x - BX, pix_y - self.bannerH),
            (pix_x - BX, pix_y - BY0)
        )
        self.banner_color = get_dye_color(color)
        draw = ImageDraw.Draw(self.mapimage)
        draw.polygon(poly_pts, fill=self.banner_color, outline='black')

        if name:
            draw.text((pix_x-1, pix_y-1), name, fill='black', anchor='ma', font=self.banner_font)
            draw.text((pix_x+1, pix_y+1), name, fill='black', anchor='ma', font=self.banner_font)
            draw.text((pix_x, pix_y), name, fill='white', anchor='ma', font=self.banner_font)

    def add_banners(self):
        print(f'Adding banners...')
        dx = 0
        dy = 0

        ### TODO : font_size should come from config
        self.banner_font_size = int(5 * self.scale)
        self.bannerW = int(10/3 * self.scale)
        self.bannerH = int(20/3 * self.scale)
        ### TODO : config should contain a list of "banner fonts" and try each until successful
        self.banner_font = ImageFont.truetype('Keyboard.ttf', size=self.banner_font_size)
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
                    self.block_w = self.mapobj.width_in_blocks()
                img = self.mapobj.create_image(scale=self.scale)
                if 'saveall' in self._config and self._config['saveall']:
                    print(f'Saving map image: map_{m}.png')
                    img.save(f'map_{m}.png')
                self.images[m] = img

        self.w = int(len(self._config['map'][0]) * self.w0)
        self.h = int(len(self._config['map']) * self.w0)
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
        self.map_background_color = self._config['background_color'] if 'background_color' in self._config else '#835432'
        self.bannerW = 6
        self.bannerH = 8


    def draw_map_borders(self):
        if not self._config['map_borders']:
            return
        nmaps = (len(self._config['map'][0]), len(self._config['map']))
        clr  = self._config['map_borders']
        line_w = 2
        draw = ImageDraw.Draw(self.mapimage)
    
        X = 0
        Y = 0
        xstep = int(self.mapimage.width/nmaps[0])
        ystep = int(self.mapimage.height/nmaps[1])
        while X < self.mapimage.width:
            draw.line([(X, 0), (X, self.mapsize[1])], fill=clr, width=line_w)
            X += xstep

        while Y < self.mapimage.height:
            draw.line([(0, Y), (self.mapsize[0], Y)], fill=clr, width=line_w)
            Y += ystep

    def draw_region_borders(self):
        if not self._config['region_borders']:
            return
        clr = self._config['region_borders']
        line_w = 3
        draw = ImageDraw.Draw(self.mapimage)
        
        X0 = int(math.floor(self.maporigin[0] / 512.0) * 512)
        Y0 = int(math.floor(self.maporigin[1] / 512.0) * 512)
        print(f'Region Origin: ({X0}, {Y0})')
        xstep = ystep = 512
        X = X0
        while X < self.mapsize[0]:
            if X >= self.maporigin[0]:
                p0 = self.block_to_map((X, 0, Y0))
                p1 = self.block_to_map((X, 0, self.mapsize[1]))
                draw.line([p0, p1], fill=clr, width=line_w)
            X += xstep
        Y = Y0
        while Y < self.mapsize[1]:
            if Y >= self.maporigin[1]:
                p0 = self.block_to_map((X0, 0, Y))
                p1 = self.block_to_map((self.mapsize[0], 0, Y))
                draw.line([p0, p1], fill=clr, width=line_w)
            Y += ystep

    def draw_village_borders(self):
        pass
