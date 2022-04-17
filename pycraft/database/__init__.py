'''
Load Minecraft data into a relational database to simplify subsequent data queries
'''
import sqlalchemy as db
import threading
import logging

class Database():
    _RECORD_ID = 0
    _RECORD_ID_LOCK = threading.Lock()
    def __init__(self, dbfile):
        self._engine = db.create_engine(f'sqlite:///{dbfile}')
        self._connection = self._engine.connect()
        self._metadata = db.MetaData(bind=self._engine)
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
        connection = self._engine.connect()
        table_obj = self._metadata.tables[table]
        query = db.insert(table_obj)
        ResultProxy = connection.execute(query, records)

    def _create_item_table(self):
        logging.info('Create Items Table')
        items = db.Table(
            'items', self._metadata,
            db.Column('Id', db.Integer(), nullable=False, primary_key=True),
            db.Column('Owner', db.String(32)),
            db.Column('Container', db.String(32)), # chest, hand, armor, ...
            db.Column('container_item', db.Integer()),
            db.Column('x', db.Integer(), nullable=False),
            db.Column('y', db.Integer(), nullable=False),
            db.Column('z', db.Integer(), nullable=False),
            db.Column('type', db.String(32), nullable=False),
            db.Column('count', db.Integer(), nullable=False),
            db.Column('slot', db.Integer(), nullable=False),
            keep_existing=True
        )

    def _create_entity_table(self):
        logging.info('Create Entities Table')
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
            db.Column('owner', db.String(32)),
            keep_existing=True
        )

    def _create_item_modifiers_table(self):
        logging.info('Create Item Modifiers Table')
        item_modifiers = db.Table(
            'item_modifiers', self._metadata,
            db.Column('item_id', db.Integer(), nullable=False),
            db.Column('modifier', db.String(32), nullable=False),
            db.Column('value', db.Integer(), nullable=False),
            db.Column('type', db.String(32)),
            keep_existing=True
        )

    def _create_villager_table(self):
        logging.info('Create Villager Table')
        villagers = db.Table(
            'villagers', self._metadata,
            db.Column('Id', db.String(32), nullable=False),
            db.Column('job', db.String(32)),
            db.Column('home_x', db.Integer()),
            db.Column('home_y', db.Integer()),
            db.Column('home_z', db.Integer()),
            db.Column('meet_x', db.Integer()),
            db.Column('meet_y', db.Integer()),
            db.Column('meet_z', db.Integer()),
            keep_existing=True
        )

    def _create_tables(self):
        self._create_entity_table()
        self._create_villager_table()
        self._create_item_table()
        self._create_item_modifiers_table()
        self._metadata.create_all(checkfirst=True)
        self._metadata.reflect()
