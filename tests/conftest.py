import copy
import pytest
from sqlalchemy import create_engine
from model.model import *
from repository.orm import metadata, start_mappers
from sqlalchemy.orm import sessionmaker, clear_mappers


@pytest.fixture
def batch():
    return Batch(reference='BATCH-01', sku='TABLE-NIZA', purchased_qty=10, eta=date.today())


@pytest.fixture
def make_batch():
    def _make_batch(eta) -> Batch:
        return Batch(reference='BATCHREF01', sku='TABLE-NIZA', purchased_qty=10, eta=eta)

    return _make_batch


@pytest.fixture
def order(customer):
    return Order('ORDER-REFERENCE', customer, [])


@pytest.fixture
def line(order):
    return OrderLine('ORDER-REFERENCE', 'TABLE-NIZA', 5)


@pytest.fixture
def customer():
    return Customer()


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    # create a configured "Session" class
    Session = sessionmaker(bind=in_memory_db)
    yield Session()
    clear_mappers()
