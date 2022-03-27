# Find the population etc of villages near the player
from pycraft import Player
from pycraft import World

import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Take a census of the user\'s region')
    parser.add_argument('worldpath', type=str, help='Path to saved world')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    player = Player(args.worldpath)
    world = World(args.worldpath)
    print(f'Player position: {player.position}')
    region = player.get_region()
    print(f' - region: {region._fname}')
    region_tags = {}
    entity_tags = {}
    poi_tags = {}

    player_pos = player.position
    print(f'PLAYER CHUNK: {player.chunk_position}')
    print(f'    Expected: 13, 12 (13, 172)')
    # chunk = world.get_chunk(player_pos, 'entities')
    # chunk_tags = chunk.get_tags()
    # if not chunk_tags:
    #     print(f'No tags in player\'s chunk')
    # else:
    #     for tag in chunk_tags:
    #         entity_tags[tag] = 1
    #         print(f'{tag}: {chunk_tags[tag]}')
    # sys.exit()

    # look at the 5 x 5 chunks surrounding the player
    print(f'-------- START 5x5')
    CHUNK_SIZE = 16
    cx0 = player_pos[0] - CHUNK_SIZE * 2
    cx1 = player_pos[0] + CHUNK_SIZE * 2
    cy0 = player_pos[2] - CHUNK_SIZE * 2
    cy1 = player_pos[2] + CHUNK_SIZE * 2
    cy = cy0
    while cy <= cy1:
        cx = cx0
        while cx <= cx1:
            cpos = (cx, player_pos[1], cy)
            cx += CHUNK_SIZE
            chunk = world.get_chunk(cpos, 'region')
            if chunk:
                chunk_tags = chunk.get_tags()
                if not chunk_tags:
                    continue
            print(f'structures: {chunk.structures}')
            # print(f' --- TAGS ---')
            # chunk.list_tags()
        cy += CHUNK_SIZE

    sys.exit()

    print(f'REGION: {region_tags.keys()}')
    print(f'ENTITY: {entity_tags.keys()}')
    print(f'   POI: {poi_tags.keys()}')
