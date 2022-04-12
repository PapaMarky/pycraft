import argparse
import os

from pycraft import Chunk
from pycraft import Database
from pycraft import Player
from pycraft.colors import get_sheep_color
from pycraft.entity import EntityFactory

def parse_args():
    parser = argparse.ArgumentParser(description='Import minecraft data into queryable database')
    parser.add_argument('dbfile', type=str, help='Database file')
    parser.add_argument('--worldpath', '-w', type=str, default=None, help='Path to saved world')
    return parser.parse_args()

def process_region(region, db):
    entity_count = {}
    for cx in range(Chunk.BLOCK_WIDTH):
        for cy in range(Chunk.BLOCK_WIDTH):
            # print(f'Loading chunk {cx}, {cy}...')
            entity_chunk = region.get_chunk('entities', cx, cy)
            entities = entity_chunk.entities
            entity_list = []
            villager_list = []
            carried_list = []
            for entity in entities:
                e = EntityFactory(entity)
                pos = e.position
                color = get_sheep_color(e.color)
                chested = e.get_attributev('ChestedHorse') == 1
                tame = e.get_attributev('Tame') == 1
                owner = e.owner
                uuid = e.uuid
                print(f'{uuid} | {e.id} | {e.get_attributev("Health")} | {pos} | {color} | {chested} | {tame} | {owner}')
                ## ArmorItems
                items = e.get_attributev('ArmorItems')
                if items:
                    slot = 0
                    for item in items:
                        if 'id' in item and 'Count' in item:
                            item_type = item['id'].value[10:]
                            count = item['Count'].value
                            print(f'     armor {slot} | {item_type} | {count}')
                            carried_list.append({
                                'Owner': uuid,
                                'Container': 'armor',
                                'type': item_type,
                                'count': count,
                                'slot': slot
                            })
                        slot += 1
                ## HandItems
                items = e.get_attributev('HandItems')
                if items:
                    slot = 0
                    for item in items:
                        if 'id' in item and 'Count' in item:
                            item_type = item['id'].value[10:]
                            count = item['Count'].value
                            print(f'     hand {slot} | {item_type} | {count}')
                            carried_list.append({
                                'Owner': uuid,
                                'Container': 'hand',
                                'type': item_type,
                                'count': count,
                                'slot': slot
                            })
                        slot += 1
                ## Items (chest)
                items = e.get_attributev('Items')
                if items:
                    for item in items:
                        if 'id' in item and 'Count' in item and 'Slot' in item:
                            item_type = item['id'].value[10:]
                            count = item['Count'].value
                            slot = item['Slot'].value
                            print(f'     slot {slot} | {item_type} | {count}')
                            carried_list.append({
                                'Owner': uuid,
                                'Container': 'chest',
                                'type': item_type,
                                'count': count,
                                'slot': slot
                            })
                # Item (contents of "item_frame" or "item")
                item = e.get_attributev('Item')
                if item:
                    if 'id' in item and 'Count' in item:
                        item_type = item['id'].value[10:]
                        count = item['Count'].value
                        slot = 0
                        print(f'     {e.id} | {slot} | {item_type} | {count}')
                        carried_list.append({
                            'Owner': uuid,
                            'Container': e.id,
                            'type': item_type,
                            'count': count,
                            'slot': slot
                        })

                entity_list.append(
                    {
                        'Id': uuid, 
                        'type': e.id, 
                        'health': e.get_attributev('Health'), 
                        'pos_x': pos[0],
                        'pos_y': pos[1],
                        'pos_z': pos[2],
                        'color': color,
                        'chested': chested,
                        'tame': tame,
                        'owner': owner
                    })
                if e.is_type('villager'):
                    home = e.home['pos'] if e.home else [None, None, None]
                    meet = e.meeting_point['pos'] if e.meeting_point else [None, None, None]
                    villager_list.append(
                        {
                            'Id': uuid,
                            'job': e.profession[10:],
                            'home_x': home[0],
                            'home_y': home[1],
                            'home_z': home[2],
                            'meet_x': meet[0],
                            'meet_y': meet[1],
                            'meet_z': meet[2]
                        })

            if len(entity_list) > 0:
                db.insert_entity_records(entity_list)
            if len(villager_list) > 0:
                db.insert_villager_records(villager_list)
            if len(carried_list) > 0:
                db.insert_carried_items_records(carried_list)

def process_player(player, db):
    pass

if __name__ == '__main__':
    args = parse_args()
    worldpath = args.worldpath if args.worldpath else os.environ.get('WORLDPATH')
    if not worldpath:
        raise Exception('World path must be specified on commandline (--worldpath) or via environment var WORLDPATH')
    if not os.path.isdir(worldpath):
        raise Exception(f'Specified world path does not exist: "{worldpath}"')
    db = Database(args.dbfile)

    # For starters, only process the player's region
    player = Player(worldpath)
    region = player.get_region()
    process_player(player, db)
    process_region(region, db)


