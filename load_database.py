import argparse
import concurrent.futures
import json
import logging
import os
import queue
import signal
import sys
import threading
import traceback

from pycraft import __version__ as pycraft_version
from pycraft import Chunk
from pycraft import Database
from pycraft import Player
from pycraft import Region
from pycraft import World
from pycraft.util import ElapsedTime
from pycraft.colors import get_sheep_color
from pycraft.entity import EntityFactory

SHUTTING_DOWN=False

def shutdown_handler(signum, frame):
    global SHUTTING_DOWN
    if not SHUTTING_DOWN:
        logging.warning(f'Got signal {signum}. Shutting down.')
        SHUTTING_DOWN=True

signal.signal(signal.SIGINT, shutdown_handler)

def parse_args():
    DEF_THREADS = 10
    parser = argparse.ArgumentParser(description='Import minecraft data into queryable database')
    parser.add_argument('dbfile', type=str, help='Database file')
    parser.add_argument('--worldpath', '-w', type=str, default=None, help='Path to saved world')
    parser.add_argument('--loglevel', '-l', type=str, default='INFO', help='Log level: DEBUG, INFO, WARN, ERROR')
    parser.add_argument('--threads', '-t', type=int, default=10, help=f'Number of threads to run. [default {DEF_THREADS}]. More than a 100 may require you to increase the open file limit using "ulimit -n NUM" on Linux')
    parser.add_argument('--playeronly', '-p', help='Load only data for the player\'s region. (default is to load all data for all regions)', action='store_true')
    return parser.parse_args()

def get_value(v):
    return v.value if str(type(v).__name__).startswith('NBT') else v

def process_item(item, owner, pos, container, container_id, item_list, modifier_list, db, slot=None, debug=False):
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
        item_id = db.next_record_id()
        damage = None
        repair_cost = None
        if 'tag' in item:
            t = item['tag']
            # Item Tag (filled_map): {'type_id': 10, 'value': {'map': {'type_id': 3, 'value': 131}}}
            imp = ('map', 'Enchantments', 'Damage', 'RepairCost', 'display', 'StoredEnchantments', 'Potion', 'Effects', 'Decorations')
            for x in t:
                if not x in imp:
                    logging.warning(f'Item Tag (in {item_type}: "{x}"): {t}')
                    logging.warning(x)
            if 'Decorations' in t:
                for decoration in t['Decorations']:
                    dec_id = f'decoration_{decoration.get("id").value}'
                    for dec in decoration:
                        if dec != 'id':
                            mod = {
                                'item_id': item_id,
                                'modifier': dec_id,
                                'value': decoration[dec].value,
                                'type': dec
                            }
                            modifier_list.append(mod)

            elif 'Effects' in t:
                effects = get_value(t['Effects'])
                for effect in effects:
                    if 'EffectId' in effect and 'EffectDuration' in effect:
                        modifier_list.append({
                            'item_id': item_id,
                            'modifier': 'effect',
                            'value': effect['EffectDuration'].value,
                            'type': effect['EffectId'].value
                        })
            elif 'Damage' in t:
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
                    data = json.loads(name)
                    if 'name' in data:
                        name = data['name']
                        modifier_list.append({
                            'item_id': item_id,
                            'modifier': 'name',
                            'value': 0,
                            'type': name
                        })
                    elif 'translate' in data:
                        name = data['translate']
                        modifier_list.append({
                            'item_id': item_id,
                            'modifier': 'name',
                            'value': 0,
                            'type': name
                        })
                    else:
                        logging.warning(f'No text in Display Tag: {t["display"]}')
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
        item = {
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
        }
        logging.info(f'Item: {item}')
        item_list.append(item)
        return item_id

def process_entity(entity, entity_list, item_list, villager_list, modifier_list, db):
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
            process_item(item, uuid, pos, 'armor', None, item_list, modifier_list, db, slot)
            slot += 1
    ## HandItems
    items = e.get_attributev('HandItems')
    if items:
        slot = 0
        for item in items:
            # print(f'HandItem: {item}')
            process_item(item, uuid, pos, 'hand', None, item_list, modifier_list, db, slot)
            slot += 1
    ## Items (chest)
    items = e.get_attributev('Items')
    if items:
        # Create an item for the entity itself
        fake_item = {'id': 'minecraft:' + e.id, 'Count': 1}
        chest_id = process_item(fake_item, uuid, pos, 'entity', None, item_list, modifier_list, db, 0)
        for item in items:
            process_item(item, uuid, pos, e.id, chest_id, item_list, modifier_list, db)

    # Item (contents of "item_frame" or "item")
    # 'item': a pile of things
    # 'item_frame': a frame that can hold items
    item = e.get_attributev('Item')
    if item:
        # Create an item for the entity itself
        fake_item = {'id': 'minecraft:' + e.id, 'Count': 1}
        entity_id = process_item(fake_item, uuid, pos, 'entity', None, item_list, modifier_list, db, 0)
        process_item(item, None, pos, e.id, entity_id, item_list, modifier_list, db, 0)

    # SaddleItem: {'type_id': 10, 'value': {'id': {'type_id': 8, 'value': 'minecraft:saddle'}, 'Count': {'type_id': 1, 'value': 1}}}
    item = e.get_attributev('SaddleItem')
    if item:
        process_item(item, uuid, pos, 'saddle', None, item_list, modifier_list, db, 0)

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

def process_entity_items(entity, item_list, modifier_list, db):
    if 'Items' in entity and len(entity['Items']) > 0:
        logging.info(f'--- ENTITY: {entity["id"].value[10:]} ({entity["x"].value}, {entity["y"].value}, {entity["z"].value})')
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
        fake_item_id = process_item(fake_item, None, pos, '', None, item_list, modifier_list, db, 0)
        if fake_item_id is not None:
            logging.info(f'Fake Entity Item: {item_list[-1:][0]}')
        for t in entity:
            # Display information about unrecognized tags ("ignore" the ones we know about)
            ignore = ('id', 'keepPacked', 'x', 'y', 'z', 'CookTime', 'BurnTime', 'CookTimeTotal', 'TransferCooldown', 'StoredEnchantments', 'Potion')
            if t in ignore:
                continue
            if t == 'RecipesUsed':
                n = len(entity[t])
                if n > 0:
                    logging.info(f'{"RecipesUsed":>10}: ({len(entity[t])})')
                    for r in entity[t]:
                        logging.info(f'{r[10:]:>15}: {entity[t][r].value}')
            elif t == 'Items':
                for item in entity[t].value:
                    process_item(item, None, pos, entity['id'].value[10:], fake_item_id, item_list, modifier_list, db)
                    # print(f'{"Slot":>10} {item["Slot"].value}: {item["id"].value[10:]} ({item["Count"].value})')
            else:
                logging.info(f'{t:>10}: {entity[t].value}')

def process_poi(region, db):
    logging.info(f'Processing POI data for region {region.pos}...')
    et = ElapsedTime()
    poi_list = []
    count = 0
    for cx in range(Chunk.BLOCK_WIDTH):
        for cy in range(Chunk.BLOCK_WIDTH):
            poi_chunk = region.get_chunk('poi', cx, cy)
            if poi_chunk:
                logging.debug(f'Loading poi chunk {cx}, {cy}...')
                sections = poi_chunk.get_tag('Sections')
                if sections is None:
                    continue
                for sec in sections:
                    if SHUTTING_DOWN:
                        return
                    # v = sections[sec]['Valid'].value
                    recs = sections[sec]['Records']
                    for rec in recs:
                        count += 1
                        pos = rec['pos'].value
                        free_tickets = rec['free_tickets'].value
                        if free_tickets is None:
                            logging.warning('free_tickets is None')
                            free_tickets = 0
                        rtype = rec['type'].value[10:]
                        poi_list.append({
                            'x': pos[0],
                            'y': pos[1],
                            'z': pos[2],
                            'type': rtype,
                            'free': free_tickets
                        })
        if len(poi_list) > 0:
            logging.info(f'adding {len(poi_list)} POIs')
            db.insert_poi_records(poi_list)
            poi_list = []
    logging.info(f'Processed {count} poi records ({et.elapsed_time_str()})')

def process_regions(region, db):
    logging.info(f'Processing Region data for region {region.pos}...')
    et = ElapsedTime()
    item_list = []
    modifier_list = []
    count = 0
    total_size = 0
    for cx in range(Chunk.BLOCK_WIDTH):
        for cy in range(Chunk.BLOCK_WIDTH):
            if SHUTTING_DOWN:
                return
            region_chunk = region.get_chunk('region', cx, cy)
            total_size += region_chunk.size
            block_entities = region_chunk.get_tag('block_entities')
            if block_entities:
                logging.info(f'Loading regions block_entities from chunk {cx}, {cy}... (chunk size: {region_chunk.size})')
                for entity in block_entities:
                    count += 1
                    process_entity_items(entity, item_list, modifier_list, db)
        if len(item_list) > 0:
            logging.info(f'adding {len(item_list)} items')
            db.insert_items_records(item_list)
            item_list = []
        if len(modifier_list) > 0:
            logging.info(f'adding {len(modifier_list)} modifiers')
            db.insert_item_modifiers_records(modifier_list)
            modifier_list = []
    logging.info(f'Processed {count} block entities in region. TOTAL SIZE: {total_size} TIME: {et.elapsed_time_str()}, {total_size/et.get_elapsed_time():.0f} BPS')

def process_entities(region, db):
    logging.info(f'Processing entities for region {region.pos}...')
    et = ElapsedTime()
    count = 0
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
                if SHUTTING_DOWN:
                    return
                count += 1
                process_entity(entity, entity_list, item_list, villager_list, modifier_list, db)

            if len(entity_list) > 0:
                logging.info(f'adding {len(entity_list)} entities')
                db.insert_entity_records(entity_list)
                entity_list = []
            if len(villager_list) > 0:
                logging.info(f'adding {len(villager_list)} villagers')
                db.insert_villager_records(villager_list)
                villager_list = []
            if len(item_list) > 0:
                logging.info(f'adding {len(item_list)} items')
                db.insert_items_records(item_list)
                item_list = []
            if len(modifier_list) > 0:
                logging.info(f'adding {len(modifier_list)} modifiers')
                db.insert_item_modifiers_records(modifier_list)
                modifier_list = []
    logging.info(f'Processed {count} entities in entities data ({et.elapsed_time_str()})')

def process_player(player, db):
    logging.info('Processing Player data...')
    et = ElapsedTime()
    item_list = []
    entity_list = []
    villager_list = []
    modifier_list = []
    vehicle = player.get_vehicle()
    if vehicle and 'Entity' in vehicle:
        entity = vehicle['Entity']
        process_entity(entity, entity_list, item_list, villager_list, modifier_list, db)
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
        i = process_item(item, player.uuid, pos, container, None, item_list, modifier_list, db, slot)

    if len(entity_list) > 0:
        db.insert_entity_records(entity_list)
    if len(item_list) > 0:
        db.insert_items_records(item_list)
    if len(villager_list) > 0:
        db.insert_villager_records(villager_list)
    if len(modifier_list) > 0:
        db.insert_item_modifiers_records(modifier_list)
    logging.info(f'Processed Player data ({et.elapsed_time_str()})')

def setup_logging(args):
    level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f'Invalid log level: {level}')
    lformat = '%(levelname)s:%(asctime)s:%(threadName)s:%(message)s'
    filename = 'load_database.log'
    logging.basicConfig(level=level, format=lformat, filename=filename)

def thread_runner(qlen, q, worldpath, dbfile):
    try:
        have_task = False
        cmdmap = {
            'player': process_player,
            'regions': process_regions,
            'entities': process_entities,
            'poi': process_poi
        }
        me = threading.current_thread()
        base_name = me.name
        db = Database(dbfile, create_tables=False)
        while True:
            if SHUTTING_DOWN:
                return False
            if q.empty():
                logging.info('No more Tasks')
                return True
            tasks_remaining = q.qsize()
            logging.info('Getting next task...')
            task = q.get()
            cmd = task.get('cmd', None)
            data = task.get('data', None)
            logging.info(f'Got task: {cmd}')
            have_task = True
            if cmd and data:
                if not cmd in cmdmap:
                    logging.error(f'BAD CMD: {cmd}')
                else:
                    # rename the thread to something useful
                    region = None
                    if cmd != 'player':
                        logging.debug(f'DATA: {data}')
                        pos = data.get('pos', None)
                        if len(pos) == 2:
                            data = Region(worldpath, pos[0], pos[1])
                        elif len(pos) == 3:
                            x, y = World.pos_to_xy(pos)
                            data = Region.from_position_xy(worldpath, x, y)
                    taskname = f'{base_name}.{cmd}' if cmd == 'player' else f'{base_name}.{cmd}{data.pos}'
                    pct = ((qlen - tasks_remaining) / qlen) * 100
                    logging.info(f'START TASK: {taskname} ({qlen - tasks_remaining} of {qlen}: {pct:.1f}%)')
                    me.name = taskname
                    cmdmap[cmd](data, db)
                    if SHUTTING_DOWN:
                        return False
                    logging.info(f'TASK COMPLETE')
                    me.name = base_name

    except Exception as e:
        logging.exception(f'##### WORKER EXCEPTION: {e}')
        for line in traceback.format_exc().splitlines():
            logging.error('> ' + line)
            logging.error(f'TASK FAILED')
            return False
    finally:
        if have_task:
            q.task_done()

def thread_launcher(**kwargs):
    logging.info('Launch Thread')
    qlen = kwargs.get('qlen', None)
    q = kwargs.get('queue', None)
    worldpath = kwargs.get('world', None)
    if q is None:
        logging.error('Queue was not passed into thread launcher')
        return False

    dbfile = kwargs.get('dbfile', None)
    if dbfile is None:
        logging.error('Database file path not passed into thread launcher')
        return False

    return thread_runner(qlen, q, worldpath, dbfile)

def setup_database(dbfile):
    '''
    Force the tables to all be created before accessing via threads.
    '''
    if os.path.exists(dbfile):
        logging.warning('DB file exists. Deleting')
        os.remove(dbfile)
    db = Database(args.dbfile)

def load_queue(worldpath, playeronly):
    q = queue.Queue()
    player = Player(worldpath)
    q.put({'cmd': 'player', 'data': player})
    if playeronly:
        pos = player.position
        data = {
            'pos': pos
        }
        q.put({'cmd': 'regions', 'data': {'pos': pos}})
        q.put({'cmd': 'entities', 'data': {'pos': pos}})
        q.put({'cmd': 'poi', 'data': {'pos': pos}})
    else:
        files = os.listdir(f'{worldpath}/region')
        # NOTE: mapping the pos to ints is not strictly necessary, but it makes the logs
        # easier to read
        for f in files:
            pos = list(map(int, f.split('.')[1:-1]))
            logging.debug(f'Adding {f}...{pos}')
            q.put({'cmd': 'regions', 'data': {'pos': pos}})
        files = os.listdir(f'{worldpath}/entities')
        for f in files:
            pos = list(map(int, f.split('.')[1:-1]))
            logging.debug(f'Adding {f}...{pos}')
            q.put({'cmd': 'entities', 'data': {'pos': pos}})
        files = os.listdir(f'{worldpath}/poi')
        for f in files:
            pos = list(map(int, f.split('.')[1:-1]))
            logging.debug(f'Adding {f}...{pos}')
            q.put({'cmd': 'poi', 'data': {'pos': pos}})
    return q

if __name__ == '__main__':
    args = parse_args()
    setup_logging(args)
    logging.info('******************************')
    logging.info(f'* START {os.path.basename(sys.argv[0])}')
    logging.info(f'* pycraft v{pycraft_version}')
    logging.info('******************************')
    main_et = ElapsedTime()
    worldpath = args.worldpath if args.worldpath else os.environ.get('WORLDPATH')
    if not worldpath:
        raise Exception('World path must be specified on commandline (--worldpath) or via environment var WORLDPATH')
    if not os.path.isdir(worldpath):
        raise Exception(f'Specified world path does not exist: "{worldpath}"')
    setup_database(args.dbfile)

    q = load_queue(worldpath, args.playeronly)
    queue_length = q.qsize()
    logging.info(f'{queue_length} Tasks to perform')
    if args.threads == 0:
        args.threads = queue_length
        logging.info(f'Setting number of threads to {queue_length}')
    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=thread_launcher, name=f'w.{i:03}', kwargs={'queue': q, 'dbfile': args.dbfile, 'qlen': queue_length, 'world': worldpath})
        t.start()
        threads.append(t)

    # wait for all of the threads to complete
    for t in threads:
        while t.is_alive():
            t.join(1)
    logging.info(f'All Done (TOTAL ELAPSED TIME: {main_et.elapsed_time_str()}')
