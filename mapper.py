## Create an image from map.dat files
from pycraft import MapImage

import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Create image files of minecraft maps')
    parser.add_argument('config_file', type=str, help='Configuration file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.config_file):
        print(f'Config file not found: "{args.config_file}"')
        sys.exit(1)
    map_image = MapImage(args.config_file)
    map_image.create_image()
    map_image.save_image('bigmap.png')
