# Find the population etc of villages near the player
from pycraft import Player
from pycraft import World
from pycraft import Entity
from pycraft.entity import EntityFactory

import argparse
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Take a census of the user\'s region')
    parser.add_argument('worldpath', type=str, help='Path to saved world')
    return parser.parse_args()

def add_entity(e, entity_count):
    if not e in entity_count:
        entity_count[e] = 0
    entity_count[e] += 1

def process_entity(e, entity_count):
    print(f'Entity: {e.id}: {e.uuid}')
    if e:
        add_entity(e.id, entity_count)
        print(f'    POS: {e.position}')
        if e.is_type('villager'):
            home = e.home['pos'] if e.home else 'HOMELESS'
            print(f'   HOME: {home}')
            job = e.profession if e.profession else 'Unemployed'
            print(f'    JOB: {job}')
            village = e.meeting_point['pos'] if e.meeting_point else 'Vagrant'
            print(f'VILLAGE: {village}')
                
        if e.owner:
            if e.owner == player._uuid:
                print(f'   Owner: PLAYER')
            else:
                print(f'  Player: {player._uuid}')
                print(f'   Owner: {e.owner}')
    
def process_entities(entities, entity_count):
    for entity in entities:
        e = EntityFactory(entity)
        process_entity(e, entity_count)

def process_region(region, player=None):
    entity_count = {}
    if player:
        v = player.get_vehicle()
        if v and 'Entity' in v:
            v_ent = EntityFactory(v['Entity'])
            process_entity(v_ent, entity_count)

    for cx in range(32):
        for cy in range(32):
            entity_chunk = region.get_chunk('entities', cx, cy)
            # print(f'    {entity_chunk.position()}')
            entities = entity_chunk.entities
            process_entities(entities, entity_count)

    for k in entity_count:
        print(f'{k:>20}: {entity_count[k]}')

if __name__ == '__main__':
    args = parse_args()
    player = Player(args.worldpath)
    print(f'Player: {player.uuid}')
    alist = player.get_attr_list()
    v = player.get_vehicle()
    if v:
        v_ent = EntityFactory(v['Entity']
                              )
        print('Player Vehicle:')
        print(f' - {v_ent.id}: {v_ent.uuid}')
        a = v_ent.owner
        if a:
            if a == player.uuid:
                print(f'        Owner: Player')
            else:
                print(f'        Owner: {a}')
        a = v_ent.get_attribute('Tame')
        if a:
            print(f'         Tame: {a.value}')
        a = v_ent.get_attribute('Leash')
        if a:
            print(f'        Leash: {a.json_obj(full_json=False)}')
        a = v_ent.chest
        if a:
            print(f'        Chest:')
            for i in a:
                t = i["id"].value
                if t.startswith('minecraft'):
                    t = t[10:]
                print(f'          - {i["Slot"].value}: {i["Count"].value} {t}')
        a = v_ent.get_attribute('SaddleItem')
        if a:
            print(f'       Saddle: {a.value}')
        # print(f'{v_ent.get_attribute_list()}')

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
    process_region(region, player)
    sys.exit(1)
    # chunk = world.get_chunk(player_pos, 'entities')
    # chunk_tags = chunk.get_tags()
    # if not chunk_tags:
    #     print(f'No tags in player\'s chunk')
    # else:
    #     for tag in chunk_tags:
    #         entity_tags[tag] = 1
    #         print(f'{tag}: {chunk_tags[tag]}')
    # sys.exit()

    # look at the N x N chunks surrounding the player
    CHUNK_SIZE = 16
    print(f'-------- START {CHUNK_SIZE*2+1}x{CHUNK_SIZE*2+1}')
    cx0 = player_pos[0] - CHUNK_SIZE * 16
    cx1 = player_pos[0] + CHUNK_SIZE * 16
    cy0 = player_pos[2] - CHUNK_SIZE * 16
    cy1 = player_pos[2] + CHUNK_SIZE * 16
    cy = cy0

    chunk_collection = {}
    entity_count = {}
    while cy <= cy1:
        cx = cx0
        while cx <= cx1:
            cpos = (cx, player_pos[1], cy)
            print(f'--- CHUNK {cx}, {cy}')
            entity_chunk = world.get_chunk(cpos, 'entities')
            # find mob data
            if entity_chunk:
                print(f'    {entity_chunk.position()}')
                entities = entity_chunk.entities
                process_entities(entities, entity_count)
            cx += CHUNK_SIZE

        cy += CHUNK_SIZE

    for k in entity_count:
        print(f'{k:>20}: {entity_count[k]}')
