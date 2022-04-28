## find items in chests, furnaces, etc
# Where things are:
# - region file
#   - furnace, blast_furnace, chest, campfire
# - entity file
#   - pack animals (unridden)
# - player data
#   - pack animal player is riding

from pycraft import Player
from pycraft import Chunk

import argparse
import math
import sys

containers = []

def parse_args():
    parser = argparse.ArgumentParser(description='Find things stored in player\'s region')
    parser.add_argument('worldpath', type=str, help='Path to saved world')
    parser.add_argument('--search', '-s', type=str, default=None, help='Comma separated list of search terms')
    parser.add_argument('--show-all', '-a', action='store_true', help='Show all items in container even if they do not match')
    parser.add_argument('--distance', '-d', default=0, type=int, help='Only show items withint "distance" of the player')
    return parser.parse_args()

def check_player(player, search, show_all, pos, dist):
    v = player.get_vehicle()
    print(f'Player vehicle: {v}')
    print('Player Inventory')
    inventory = player.inventory
    show = True
    if search and len(search) > 0:
        show = False
        for item in player.inventory:
            for s in search:
                if s in item['id'][10:]:
                    show = True
                    break
    if show:
        e_id = item['id'][10:]

        print(f'{e_id} at ({pos[0]}, {pos[1]}, {pos[2]})')
        for i in player.inventory:
            matched = ' '
            for s in search:
                if s in i['id'][10:]:
                    matched = '*'
            if show_all or matched == '*':
                print(f'  {matched}Slot {i["Slot"]}: {i["Count"]} {i["id"][10:]}')


def check_items(e, search, show_all, pos, dist):
    if 'Items' in e:
        if len(e['Items']) > 0:
            x = y = z = None
            ditem = None
            if 'Pos' in e:
                p = e['Pos']
                x = int(p[0].value)
                y = int(p[1].value)
                z = int(p[2].value)
            else:
                x = e['x'].value
                y = e['y'].value
                z = e['z'].value

            dist_str = ''
            ditem = abs((x - pos[0]) * (x - pos[0]) + (y - pos[1]) * (y - pos[1]) + (z - pos[2]) * (z - pos[2]))
            if dist > 0 and ditem > dist:
                return
            dist_str = f' distance: {int(math.sqrt(ditem))}'
            show = True
            if search and len(search) > 0:
                show = False
                for item in e['Items']:
                    for s in search:
                        if s in item['id'].value[10:]:
                            show = True
                            break
            if show:
                print('----------')
                e_id = e['id'].value[10:]

                print(f'{e_id} at ({x}, {y}, {z}){dist_str}')
                for i in e["Items"]:
                    matched = ' '
                    for s in search:
                        if s in i['id'].value[10:]:
                            matched = '*'
                    if show_all or matched == '*':
                        print(f'  {matched}Slot {i["Slot"].value}: {i["Count"].value} {i["id"].value[10:]}')

def check_entity_data(region, search, show_all, pos, dist):
    print('Searching Entities Data...')
    for cy in range(Chunk.BLOCK_WIDTH):
        for cx in range(Chunk.BLOCK_WIDTH):
            # check region data
            chunk = region.get_r_chunk('entities', cx, cy)
            # print(f'--- c {cx} {cy} ---')
            for e in chunk.entities:
                check_items(e, search, show_all, pos, dist)

def check_region_data(region, search, show_all, pos, dist):
    print('Searching Region Data...')
    for cy in range(Chunk.BLOCK_WIDTH):
        for cx in range(Chunk.BLOCK_WIDTH):
            # check region data
            rchunk = region.get_r_chunk('region', cx, cy)
            # print(f'--- c {cx} {cy} ---')
            entities = rchunk.get_tag('block_entities')
            for e in entities:
                check_items(e, search, show_all, pos, dist)

if __name__ == '__main__':
    args = parse_args()
    player = Player(args.worldpath)
    print(f'Player: {player.uuid}')
    print(f'Player position: {player.position}')
    search = None
    if args.search:
        search = args.search.split(',')

    print(args.search)
    print(f'Searching...')
    if search:
       print(f' Match {search}')

    dist = args.distance * args.distance
    check_player(player, search, args.show_all, player.position, dist)

    region = player.get_region()
    check_region_data(region, search, args.show_all, player.position, dist)
    check_entity_data(region, search, args.show_all, player.position, dist)
