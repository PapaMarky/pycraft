import argparse
import os
import sys

from pycraft import Chunk
from pycraft import Database
from pycraft import Player
from pycraft.colors import get_sheep_color
from pycraft.entity import EntityFactory

### NOTES
# Items can have "tags": 'Damage', 'RepairCost', 'Enchantments', etc
# ------------------------------
# ITEM: {'Slot': 30, 'id': 'minecraft:iron_axe', 'Count': 1, 'tag': {'Damage': 111, 'RepairCost': 0}}
# ITEM: {'Slot': 32, 'id': 'minecraft:black_wool', 'Count': 64}
# ITEM: {'Slot': 34, 'id': 'minecraft:torch', 'Count': 16}
# ITEM: {'Slot': 35, 'id': 'minecraft:smooth_stone_slab', 'Count': 43}
# ITEM: {'Slot': 100, 'id': 'minecraft:golden_boots', 'Count': 1, 'tag': {'Damage': 15, 'Enchantments': [{'lvl': 3, 'id': 'minecraft:depth_strider'}]}}
# ITEM: {'Slot': 101, 'id': 'minecraft:leather_leggings', 'Count': 1, 'tag': {'Damage': 0, 'display': {'color': 12687579}}}
# ITEM: {'Slot': 102, 'id': 'minecraft:iron_chestplate', 'Count': 1, 'tag': {'Damage': 45, 'Enchantments': [{'lvl': 3, 'id': 'minecraft:fire_protection'}]}}
# ITEM: {'Slot': 103, 'id': 'minecraft:golden_helmet', 'Count': 1, 'tag': {'Damage': 9, 'Enchantments': [{'lvl': 3, 'id': 'minecraft:respiration'}]

def parse_args():
    parser = argparse.ArgumentParser(description='Import minecraft data into queryable database')
    parser.add_argument('dbfile', type=str, help='Database file')
    parser.add_argument('--worldpath', '-w', type=str, default=None, help='Path to saved world')
    return parser.parse_args()

def process_item(item, owner, container, item_list, modifier_list, slot=None):
    if slot is None and not 'Slot' in item:
        return None
    slot = slot if slot is not None else item['Slot'].value
    if 'id' in item and 'Count' in item:
        item_type = item['id'][10:] if isinstance(item['id'], str) else item['id'].value[10:]
        count = item['Count'] if isinstance(item['Count'], int) else item['Count'].value
        damage = None
        repair_cost = None
        if 'tag' in item:
            t = item['tag']
            # Item Tag (filled_map): {'type_id': 10, 'value': {'map': {'type_id': 3, 'value': 131}}}
            imp = ('map', 'Enchantments', 'Damage', 'RepairCost', 'display')
            for x in t:
                if not x in imp:
                    print(f'Item Tag ({item_type}): {item["tag"]}')
                    print(x)
            if 'Damage' in t:
                damage = t['Damage']
                modifier_list.append({
                    'Owner': owner,
                    'Container': container,
                    'slot': slot,
                    'modifier': 'damage',
                    'value': damage,
                    'type': None
                })
            if 'RepairCost' in t:
                repair_cost = t['RepairCost']
                modifier_list.append({
                    'Owner': owner,
                    'Container': container,
                    'slot': slot,
                    'modifier': 'repair_cost',
                    'value': repair_cost,
                    'type': None
                })
            if 'map' in t:
                modifier_list.append({
                    'Owner': owner,
                    'Container': container,
                    'slot': slot,
                    'modifier': 'map',
                    'value': t['map'].value,
                    'type': None
                })
            if 'display' in t  and 'color' in t['display']:
                color = t['display']['color']
                modifier_list.append({
                    'Owner': owner,
                    'Container': container,
                    'slot': slot,
                    'modifier': 'display',
                    'value': color,
                    'type': None
                })

            if 'Enchantments' in t:
                for enchant in t['Enchantments']:
                    if 'id' in enchant and 'lvl' in enchant:
                        modifier_list.append({
                            'Owner': owner,
                            'Container': container,
                            'slot': slot,
                            'modifier': 'enchantment',
                            'value': enchant['lvl'],
                            'type': enchant['id'][10:] if enchant['id'].startswith('minecraft:') else enchant['id']
                        })
            item_list.append({
                'Owner': owner,
                'Container': container,
                'type': item_type,
                'count': count,
                'slot': slot
            })

def process_entity(entity, entity_list, carried_list, villager_list, modifier_list):
    e = EntityFactory(entity)
    pos = e.position
    color = get_sheep_color(e.color)
    chested = e.get_attributev('ChestedHorse') == 1
    tame = e.get_attributev('Tame') == 1
    owner = e.owner
    uuid = e.uuid
    # print(f'{uuid} | {e.id} | {e.get_attributev("Health")} | {pos} | {color} | {chested} | {tame} | {owner}')
    ## ArmorItems
    items = e.get_attributev('ArmorItems')
    if items:
        slot = 0
        for item in items:
            # print(f'ArmorItem: {item}')
            i = process_item(item, uuid, 'armor', carried_list, modifier_list, slot)
            slot += 1
    ## HandItems
    items = e.get_attributev('HandItems')
    if items:
        slot = 0
        for item in items:
            # print(f'HandItem: {item}')
            i = process_item(item, uuid, 'hand', carried_list, modifier_list, slot)
            slot += 1
    ## Items (chest)
    items = e.get_attributev('Items')
    if items:
        for item in items:
            # print(f'ChestItem: {item}')
            i = process_item(item, uuid, 'chest', carried_list, modifier_list)

    # Item (contents of "item_frame" or "item")
    item = e.get_attributev('Item')
    if item:
        i = process_item(item, uuid, e.id, carried_list, modifier_list, 0)
    # SaddleItem: {'type_id': 10, 'value': {'id': {'type_id': 8, 'value': 'minecraft:saddle'}, 'Count': {'type_id': 1, 'value': 1}}}
    item = e.get_attributev('SaddleItem')
    if item:
        i = process_item(item, uuid, 'saddle', carried_list, modifier_list, 0)

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
            modifier_list = []
            for entity in entities:
                process_entity(entity, entity_list, carried_list, villager_list, modifier_list)

            if len(entity_list) > 0:
                db.insert_entity_records(entity_list)
            if len(villager_list) > 0:
                db.insert_villager_records(villager_list)
            if len(carried_list) > 0:
                db.insert_carried_items_records(carried_list)
            if len(modifier_list) > 0:
                db.insert_item_modifiers_records(modifier_list)

def process_player(player, db):
    carried_list = []
    entity_list = []
    villager_list = []
    modifier_list = []
    vehicle = player.get_vehicle()
    if vehicle and 'Entity' in vehicle:
        entity = vehicle['Entity']
        process_entity(entity, entity_list, carried_list, villager_list, modifier_list)
    pos = player.position
    entity_list.append({
        'Id': player.uuid,
        'type': 'player',
        'health': player.get_attr('Health').value,
        'pos_x': pos[0],
        'pos_y': pos[1],
        'pos_z': pos[2],
        'color': None,
        'chested': False,
        'tame': False,
        'owner': None
    })

    for item in player.inventory:
        slot = None
        container = 'inventory'
        if 'Slot' in item:
            slot = item['Slot']
            if slot >= 100:
                container = 'armor'
                slot = slot - 100
            elif slot == -106:
                container = 'hand'
                slot = 0
        i = process_item(item, player.uuid, container, carried_list, modifier_list, slot)

    if len(entity_list) > 0:
        db.insert_entity_records(entity_list)
    if len(carried_list) > 0:
        db.insert_carried_items_records(carried_list)
    if len(villager_list) > 0:
        db.insert_villager_records(villager_list)
    if len(modifier_list) > 0:
        db.insert_item_modifiers_records(modifier_list)

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
