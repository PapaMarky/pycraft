'''
Load Minecraft data into a relational database to simplify subsequent data queries
'''
import sqlalchemy as db
import threading

class Database():
    _RECORD_ID = 0
    _RECORD_ID_LOCK = threading.Lock()
    def __init__(self, dbfile):
        self._engine = db.create_engine(f'sqlite:///{dbfile}')
        self._connection = self._engine.connect()
        self._metadata = db.MetaData()
        self._tables = {}
        self._create_tables()

    def next_record_id():
        with Database._RECORD_ID_LOCK:
            Database._RECORD_ID += 1
            return Database._RECORD_ID

    def insert_entity_records(self, records):
        self.insert_records('entities', records)

    def insert_villager_records(self, records):
        self.insert_records('villagers', records)

    def insert_items_records(self, records):
        self.insert_records('items', records)

    def insert_item_modifiers_records(self, records):
        self.insert_records('item_modifiers', records)

    def insert_records(self, table, records):
        query = db.insert(self._tables[table])
        ResultProxy = self._connection.execute(query, records)

    def _create_item_table(self):
        items = db.Table(
            'items', self._metadata,
            db.Column('Id', db.Integer(), nullable=False),
            db.Column('Owner', db.String(32)),
            db.Column('Container', db.String(32)), # chest, hand, armor, ...
            db.Column('container_item', db.Integer()),
            db.Column('x', db.Integer(), nullable=False),
            db.Column('y', db.Integer(), nullable=False),
            db.Column('z', db.Integer(), nullable=False),
            db.Column('type', db.String(32), nullable=False),
            db.Column('count', db.Integer(), nullable=False),
            db.Column('slot', db.Integer(), nullable=False)
        )
        self._tables['items'] = items

    def _create_entity_table(self):
        entities = db.Table(
            'entities', self._metadata,
            db.Column('Id', db.String(32), nullable=False),
            db.Column('type', db.String(32), nullable=False),
            db.Column('health', db.Integer()),
            db.Column('pos_x', db.Float()),
            db.Column('pos_y', db.Float()),
            db.Column('pos_z', db.Float()),
            db.Column('color', db.String(32)),
            db.Column('chested', db.Boolean()),
            db.Column('tame', db.Boolean()),
            db.Column('owner', db.String(32))
        )
        self._tables['entities'] = entities

    def _create_item_modifiers_table(self):
        item_modifiers = db.Table(
            'item_modifiers', self._metadata,
            db.Column('item_id', db.Integer(), nullable=False),
            db.Column('modifier', db.String(32), nullable=False),
            db.Column('value', db.Integer(), nullable=False),
            db.Column('type', db.String(32))
        )
        self._tables['item_modifiers'] = item_modifiers

    def _create_villager_table(self):
        villagers = db.Table(
            'villagers', self._metadata,
            db.Column('Id', db.String(32), nullable=False),
            db.Column('job', db.String(32)),
            db.Column('home_x', db.Integer()),
            db.Column('home_y', db.Integer()),
            db.Column('home_z', db.Integer()),
            db.Column('meet_x', db.Integer()),
            db.Column('meet_y', db.Integer()),
            db.Column('meet_z', db.Integer())
        )
        self._tables['villagers'] = villagers

    def _create_tables(self):
        self._create_entity_table()
        self._create_villager_table()
        self._create_item_table()
        self._create_item_modifiers_table()
        self._metadata.create_all(self._engine)
