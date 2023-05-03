from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Sequence
)
from sqlalchemy.sql import func
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)

PROPS_ID = Sequence('props_id_seq')

class Prop(Base):
    __tablename__ = "props"

    id = Column(Integer, primary_key=True, server_default=PROPS_ID.next_value())
    title = Column('title', String(100), unique=False)
    url = Column('url', String(100), unique=True)
    m2_total = Column('m2_total', Float, unique=False)
    m2_cub = Column('m2_cub', Float, unique=False)
    direction = Column('direction', String(100), unique=False)
    price = Column('price', Float, unique=False)
    original_price = Column('original_price', Float, unique=False)
    expens = Column('expens', Float, unique=False)
    currency = Column('currency', String(5), unique=False)
    location = Column('location', String(100), unique=False)
    rooms = Column('rooms', Float, unique=False)
    bedrooms = Column('bedrooms', Float, unique=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
