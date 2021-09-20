from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper
from model.model import *

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(255)),
)


def start_mappers():
    mapper(OrderLine, order_lines)
