import os

import psycopg2
import sqlalchemy
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigDatabase(metaclass=Singleton):
    engine: Engine = None
    connection: Connection = None
    session: Session = None

    def __init__(self):
        self.hostname = os.environ['DB_HOST']
        self.user = os.environ['DB_USER']
        self.password = os.environ['DB_PASSWORD']
        self.dbname = os.environ['DB_NAME']
        self.port = os.environ['DB_PORT']

        self.engine = sqlalchemy.create_engine(
            f'postgresql://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.dbname}')
        self.connection = self.engine.connect()
        self.session = Session(bind=self.connection)

    def connect(self):
        conn = psycopg2.connect(
            host=self.hostname,
            dbname=self.dbname,
            port=self.port,
            user=self.user,
            password=self.password
        )

        conn.autocommit = True
        cur = conn.cursor()
        return cur


class FileUploader(Base):
    __tablename__ = 'postcodes_fileuploader'

    id = Column(Integer, primary_key=True)
    file = Column(String)
    processed = Column(Boolean)
    updated_at = Column(TIMESTAMP)


class PostCode(Base):
    __tablename__ = 'postcode_raw'
    __table_args__ = {'schema': 'postcode'}

    id = Column(Integer, primary_key=True)
    lat = Column(Integer)
    lon = Column(Integer)


class PostCodeRAW(Base):
    __tablename__ = 'postcode_json_raw'
    __table_args__ = {'schema': 'postcode'}

    id = Column(Integer, primary_key=True)
    postcode_id = Column(Integer, ForeignKey('postcode.postcode_raw.id'))
    data_type = Column(String, nullable=True)
    json_data = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP)

    postcode = relationship("PostCode", primaryjoin="PostCode.id == PostCodeRAW.postcode_id")


class Code(Base):
    __tablename__ = 'postcodes_code'

    id = Column(Integer, primary_key=True)
    postcode = Column(String)
    country = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)
    created_at = Column(TIMESTAMP)
