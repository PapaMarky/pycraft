'''
Load Minecraft data into a relational database to simplify subsequent data queries
'''
import sqlalchemy as db
import threading
import logging

DATABASE_LOCK = threading.Lock()


class Database():
    def __init__(self, dbfile, create_tables=True):
        with DATABASE_LOCK:
            self._engine = db.create_engine(f'sqlite:///{dbfile}')
            self._connection = self._engine.connect()
            self._metadata = db.MetaData(bind=self._engine)
        if create_tables:
            self._create_tables()
        with DATABASE_LOCK:
            self._metadata.reflect()

    def next_record_id(self):
        with DATABASE_LOCK:
            with self._engine.begin() as connection:
                table_obj = self._metadata.tables['nextid']
                query = db.select(table_obj)
                result = connection.execute(query)
                rows = result.fetchall()
                if len(rows) != 1:
                    raise Exception(f'Next Id has {len(rows)} rows')
                next_id = rows[0]['next_id']
                query = db.update(table_obj)
                connection.execute(query, {'id': 0, 'next_id': next_id + 1})
                return next_id

    def insert_entity_records(self, records):
        self.insert_records('entities', records)

    def insert_villager_records(self, records):
        self.insert_records('villagers', records)

    def insert_items_records(self, records):
        self.insert_records('items', records)

    def insert_item_modifiers_records(self, records):
        self.insert_records('item_modifiers', records)

    def insert_poi_records(self, records):
        self.insert_records('poi', records)

    def insert_record(self, table, record):
        try:
            with DATABASE_LOCK:
                with self._engine.begin() as connection:
                    table_obj = self._metadata.tables[table]
                    query = db.insert(table_obj)
                    ResultProxy = connection.execute(query, record)
        except Exception as e:
            logging.error(f'Exception inserting records into "{table}": {e}')

    def insert_records(self, table, records):
        try:
            with DATABASE_LOCK:
                with self._engine.begin() as connection:
                    table_obj = self._metadata.tables[table]
                    query = db.insert(table_obj)
                    ResultProxy = connection.execute(query, records)
        except Exception as e:
            logging.error(f'Exception inserting records into "{table}": {e}')
            for record in records:
                logging.error(f' - {record}')

    def _create_poi_table(self):
        logging.info('Create POI Table')
        poi = db.Table(
            'poi', self._metadata,
            db.Column('x', db.Integer(), nullable=False),
            db.Column('y', db.Integer(), nullable=False),
            db.Column('z', db.Integer(), nullable=False),
            db.Column('type', db.String(32), nullable=False),
            db.Column('free', db.Integer(), nullable=False),
            keep_existing=True
        )

    def _create_item_table(self):
        logging.info('Create Items Table')
        items = db.Table(
            'items', self._metadata,
            db.Column('Id', db.Integer(), nullable=False, primary_key=True),
            db.Column('Owner', db.String(32)),
            db.Column('Container', db.String(32)),  # chest, hand, armor, ...
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

    def _create_nextid_table(self):
        logging.info('Create Id Table')
        nextid = db.Table(
            'nextid', self._metadata,
            db.Column('id', db.Integer(), nullable=False),
            db.Column('next_id', db.Integer(), nullable=False),
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
        self._metadata.reflect()
        self._create_entity_table()
        self._create_villager_table()
        self._create_item_table()
        self._create_item_modifiers_table()
        self._create_poi_table()
        self._create_nextid_table()
        self._metadata.create_all(checkfirst=True)
        self._metadata.reflect()
        # initialize id table
        self.insert_record('nextid', {'id': 0, 'next_id': 1})
