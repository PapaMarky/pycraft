import argparse
import json
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

def get_value(v):
    return v.value if str(type(v).__name__).startswith('NBT') else v

def process_item(item, owner, pos, container, container_id, item_list, modifier_list, slot=None, debug=False):
    if slot is None and not 'Slot' in item:
        return None
    slot = slot if slot is not None else item['Slot'].value
    if debug:
        print(f'process_item:')
        print(f'       item: {item}')
        print(f'       slot: {slot}')
        print(f'      owner: {owner}')
        print(f'  container: {container}')
        print(f' container_id: {container_id}')
    if 'id' in item and 'Count' in item:
        item_type = get_value(item['id'])[10:]
        count = item['Count'] if isinstance(item['Count'], int) else item['Count'].value
        item_id = Database.next_record_id()
        damage = None
        repair_cost = None
        if 'tag' in item:
            t = item['tag']
            # Item Tag (filled_map): {'type_id': 10, 'value': {'map': {'type_id': 3, 'value': 131}}}
            imp = ('map', 'Enchantments', 'Damage', 'RepairCost', 'display', 'StoredEnchantments', 'Potion')
            for x in t:
                if not x in imp:
                    print(f'Item Tag ({item_type}): {item["tag"]}')
                    print(x)
            if 'Damage' in t:
                damage = get_value(t['Damage'])
                modifier_list.append({
                    'item_id': item_id,
                    'modifier': 'damage',
                    'value': damage,
                    'type': None
                })
            if 'RepairCost' in t:
                repair_cost = get_value(t['RepairCost'])
                modifier_list.append({
                    'item_id': item_id,
                    'modifier': 'repair_cost',
                    'value': repair_cost,
                    'type': None
                })
            if 'map' in t:
                modifier_list.append({
                    'item_id': item_id,
                    'modifier': 'map',
                    'value': t['map'].value,
                    'type': None
                })
            if 'display' in t:
                if 'color' in t['display']:
                    color = get_value(t['display']['color'])
                    modifier_list.append({
                        'item_id': item_id,
                        'modifier': 'color',
                        'value': color,
                        'type': None
                    })
                if 'Name' in t['display']:
                    name = get_value(t['display']['Name'])
                    name = json.loads(name)['text']
                    modifier_list.append({
                        'item_id': item_id,
                        'modifier': 'name',
                        'value': 0,
                        'type': name
                    })
            if 'Potion' in t:
                potion = t['Potion']
                potion_type = get_value(potion)
                modifier_list.append({
                    'item_id': item_id,
                    'modifier': 'potion',
                    'value': 0,
                    'type': potion_type[10:] if potion_type.startswith('minecraft:') else potion_type
                })
            if 'Enchantments' in t:
                for enchant in t['Enchantments']:
                    if 'id' in enchant and 'lvl' in enchant:
                        enchant_type = get_value(enchant['id'])
                        value = get_value(enchant['lvl'])
                        modifier_list.append({
                            'item_id': item_id,
                            'modifier': 'enchantment',
                            'value': value,
                            'type': enchant_type[10:] if enchant_type.startswith('minecraft:') else enchant_type
                        })
            if 'StoredEnchantments' in t:
                for enchant in t['StoredEnchantments']:
                    if 'id' in enchant and 'lvl' in enchant:
                        enchant_type = get_value(enchant['id'])
                        value = get_value(enchant['lvl'])
                        modifier_list.append({
                            'item_id': item_id,
                            'modifier': 'stored enchantment',
                            'value': value,
                            'type': enchant_type[10:] if enchant_type.startswith('minecraft:') else enchant_type
                        })
        item_list.append({
            'Id': item_id,
            'Owner': owner,
            'Container': container,
            'container_item': container_id,
            'x': pos[0],
            'y': pos[1],
            'z': pos[2],
            'type': item_type,
            'count': count,
            'slot': slot
        })
        return item_id

def process_entity(entity, entity_list, item_list, villager_list, modifier_list):
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
            process_item(item, uuid, pos, 'armor', None, item_list, modifier_list, slot)
            slot += 1
    ## HandItems
    items = e.get_attributev('HandItems')
    if items:
        slot = 0
        for item in items:
            # print(f'HandItem: {item}')
            process_item(item, uuid, pos, 'hand', None, item_list, modifier_list, slot)
            slot += 1
    ## Items (chest)
    items = e.get_attributev('Items')
    if items:
        # Create an item for the entity itself
        fake_item = {'id': 'minecraft:' + e.id, 'Count': 1}
        chest_id = process_item(fake_item, uuid, pos, 'entity', None, item_list, modifier_list, 0)
        for item in items:
            process_item(item, uuid, pos, e.id, chest_id, item_list, modifier_list)

    # Item (contents of "item_frame" or "item")
    # 'item': a pile of things
    # 'item_frame': a frame that can hold items
    item = e.get_attributev('Item')
    if item:
        # Create an item for the entity itself
        fake_item = {'id': 'minecraft:' + e.id, 'Count': 1}
        entity_id = process_item(fake_item, uuid, pos, 'entity', None, item_list, modifier_list, 0)
        process_item(item, None, pos, e.id, entity_id, item_list, modifier_list, 0)

    # SaddleItem: {'type_id': 10, 'value': {'id': {'type_id': 8, 'value': 'minecraft:saddle'}, 'Count': {'type_id': 1, 'value': 1}}}
    item = e.get_attributev('SaddleItem')
    if item:
        process_item(item, uuid, pos, 'saddle', None, item_list, modifier_list, 0)

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

def process_entity_items(entity, item_list, modifier_list):
    if 'Items' in entity and len(entity['Items']) > 0:
        print(f'--- ENTITY: {entity["id"].value[10:]} ({entity["x"].value}, {entity["y"].value}, {entity["z"].value})')
        x = y = z = None
        if 'Pos' in entity:
            p = entity['Pos']
            x = int(p[0].value)
            y = int(p[1].value)
            z = int(p[2].value)
        else:
            x = entity['x'].value
            y = entity['y'].value
            z = entity['z'].value
        pos = [x, y, z]
        fake_item = {
            'id': entity['id'],
            'Count': 1
        }
        fake_item_id = process_item(fake_item, None, pos, '', None, item_list, modifier_list, 0)
        for t in entity:
            # Display information about unrecognized tags ("ignore" the ones we know about)
            ignore = ('id', 'keepPacked', 'x', 'y', 'z', 'CookTime', 'BurnTime', 'CookTimeTotal', 'TransferCooldown', 'StoredEnchantments', 'Potion')
            if t in ignore:
                continue
            if t == 'RecipesUsed':
                n = len(entity[t])
                if n > 0:
                    print(f'{"RecipesUsed":>10}: ({len(entity[t])})')
                    for r in entity[t]:
                        print(f'{r[10:]:>15}: {entity[t][r].value}')
            elif t == 'Items':
                for item in entity[t].value:
                    process_item(item, None, pos, entity['id'].value[10:], fake_item_id, item_list, modifier_list)
                    # print(f'{"Slot":>10} {item["Slot"].value}: {item["id"].value[10:]} ({item["Count"].value})')
            else:
                print(f'{t:>10}: {entity[t].value}')

def process_regions(region, db):
    item_list = []
    modifier_list = []
    for cx in range(Chunk.BLOCK_WIDTH):
        for cy in range(Chunk.BLOCK_WIDTH):
            # print(f'Loading chunk {cx}, {cy}...')
            region_chunk = region.get_chunk('region', cx, cy)
            block_entities = region_chunk.get_tag('block_entities')
            for entity in block_entities:
                process_entity_items(entity, item_list, modifier_list)
    if len(item_list) > 0:
        db.insert_items_records(item_list)
    if len(modifier_list) > 0:
        # for mod in modifier_list:
        #     print(f'MOD: {mod}')
        db.insert_item_modifiers_records(modifier_list)

def process_entities(region, db):
    for cx in range(Chunk.BLOCK_WIDTH):
        for cy in range(Chunk.BLOCK_WIDTH):
            # print(f'Loading chunk {cx}, {cy}...')
            entity_chunk = region.get_chunk('entities', cx, cy)
            entities = entity_chunk.entities
            entity_list = []
            villager_list = []
            item_list = []
            modifier_list = []
            for entity in entities:
                process_entity(entity, entity_list, item_list, villager_list, modifier_list)

            if len(entity_list) > 0:
                db.insert_entity_records(entity_list)
            if len(villager_list) > 0:
                db.insert_villager_records(villager_list)
            if len(item_list) > 0:
                db.insert_items_records(item_list)
            if len(modifier_list) > 0:
                db.insert_item_modifiers_records(modifier_list)

def process_player(player, db):
    item_list = []
    entity_list = []
    villager_list = []
    modifier_list = []
    vehicle = player.get_vehicle()
    if vehicle and 'Entity' in vehicle:
        entity = vehicle['Entity']
        process_entity(entity, entity_list, item_list, villager_list, modifier_list)
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
        i = process_item(item, player.uuid, pos, container, None, item_list, modifier_list, slot)

    if len(entity_list) > 0:
        db.insert_entity_records(entity_list)
    if len(item_list) > 0:
        db.insert_items_records(item_list)
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
    process_regions(region, db)
    process_entities(region, db)
