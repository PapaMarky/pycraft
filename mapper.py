## Create an images from map.dat files
from minecraft import World
from PIL import Image

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

if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.config_file):
        print(f'Config file not found: "{args.config_file}"')
        sys.exit(1)
    config = load_config(args.config_file)
    world = World(config['path'])
    images = {}
    w0 = None
    scale = config['scale'] if 'scale' in config else 1.0
    print(f'Scale: {scale}')
    for row in config['map']:
        print('--row--')
        for m in row:
            print(f'-- map {m} --')
            mapobj = world.get_map(m)
            if w0 is None:
                w0 = mapobj.get_width() * scale
            mdata = mapobj.get_data()
            img = mapobj.create_image(scale=scale)
            img.save(f'map_{m}.png')
            images[m] = img

    w = int(len(config['map'][0]) * w0)
    h = int(len(config['map']) * w0)
    mapimage = Image.new(mode="RGBA", size=(w, h))
    dx = 0
    dy = 0
    for row in config['map']:
        dx = 0
        for m in row:
            print(f'--- paste {m} ---')
            mapimage.paste(images[m], (int(dx), int(dy)))
            dx += w0
        dy += w0

    # for x in range(len(images[0])):
    #     for y in range(len(images)):
    #         dx = x * w0
    #         dy = y * w0
    #         mapimage.paste(images[x][y], (dx, dy))
    fname = f'bigmap.png'
    print(f'Writing map to {fname}')
    mapimage.save(fname)
            
