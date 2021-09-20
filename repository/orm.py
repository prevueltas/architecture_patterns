from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
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

purchased_qty = Column("purchased_qty", Integer, nullable=False)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255), unique=True),
    Column("sku", String(255)),
    purchased_qty,
    Column("eta", Date, nullable=True)
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper(OrderLine, order_lines)
    mapper(
        Batch,
        batches,
        properties={
            "_purchased_qty": purchased_qty,
            "_lines": relationship(lines_mapper, secondary=allocations, collection_class=set)
        }
    )
