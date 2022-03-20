## Create an images from map.dat files
from minecraft import World
from minecraft.colors import get_dye_color

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

import argparse
import json
import math
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Create image files of minecraft maps')
    parser.add_argument('config_file', type=str, help='Configuration file')
    return parser.parse_args()

def load_config(config_file):
    with open(config_file) as cfile:
        return json.loads(cfile.read())

def draw_banner(banner, img, maporigin, mapsize, font, bannerW=6, bannerH=8):
    pos = banner['pos']
    color = banner['color']
    name = banner['name']
    ox = maporigin[0]
    oz = maporigin[1]
    x_pct = (pos[0] - ox) / mapsize[0]
    y_pct = (pos[2] - oz) / mapsize[1]
    pix_x = int(x_pct * img.width)
    pix_y = int(y_pct * img.height)
    BX = int(bannerW/2)
    BY0 = int(bannerH/3)
    poly_pts = (
        (pix_x, pix_y),
        (pix_x + BX, pix_y - BY0),
        (pix_x + BX, pix_y - bannerH),
        (pix_x - BX, pix_y - bannerH),
        (pix_x - BX, pix_y - BY0)
    )
    banner_color = get_dye_color(color)
    draw = ImageDraw.Draw(img)
    draw.polygon(poly_pts, fill=banner_color, outline='black')

    if name:
        draw.text((pix_x-1, pix_y-1), name, fill='black', anchor='ma', font=font)
        draw.text((pix_x+1, pix_y+1), name, fill='black', anchor='ma', font=font)
        draw.text((pix_x, pix_y), name, fill='white', anchor='ma', font=font)

if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.config_file):
        print(f'Config file not found: "{args.config_file}"')
        sys.exit(1)
    config = load_config(args.config_file)
    world = World(config['path'])
    images = {}
    w0 = None
    block_w = None
    scale = config['scale'] if 'scale' in config else 1.0
    print(f'Scale: {scale}')
    row_num = 0
    for row in config['map']:
        print(f'--row {row_num}--')
        row_num += 1
        for m in row:
            print(f'-- map {m} --')
            mapobj = world.get_map(m)
            if w0 is None:
                w0 = mapobj.get_width() * scale
                block_w = mapobj.width_in_blocks()
            img = mapobj.create_image(scale=scale)
            if 'saveall' in config and config['saveall']:
                img.save(f'map_{m}.png')
            images[m] = img

    w = int(len(config['map'][0]) * w0)
    h = int(len(config['map']) * w0)

    # select 102, 76, 51 as background color to mimic maps in a frame
    back = config['background_color'] if 'background_color' in config else '#835432'
    mapimage = Image.new(mode="RGBA", size=(w, h), color=back)
    dx = 0
    dy = 0
    for row in config['map']:
        dx = 0
        for m in row:
            # TODO : learn how to use "mask" so I can use alpha channels
            mapimage.paste(images[m], (int(dx), int(dy)), images[m])
            dx += w0
        dy += w0
    print(f'Adding banners...')
    dx = 0
    dy = 0
    map_0_0 = world.get_map(config['map'][0][0])
    maporigin = map_0_0.get_origin()
    mapsize = (len(config['map'][0]) * block_w, len(config['map']) * block_w)

    font_size = int(5 * scale)
    bannerW = int(10/3 * scale)
    bannerH = int(20/3 * scale)
    font = ImageFont.truetype('Keyboard.ttf', size=font_size)
    for row in config['map']:
        for m in row:
            mapobj = world.get_map(m)
            banners = mapobj.get_banners()
            for banner in banners:
                draw_banner(banner, mapimage, maporigin, mapsize, font, bannerW=bannerW, bannerH=bannerH)
            dx += w0
        dy += w0

    fname = f'bigmap.png'
    print(f'Writing map to {fname}')
    mapimage.save(fname)
