import copy
import pytest
from model.model import *


@pytest.fixture
def batch():
    return Batch(reference='BATCH-01', sku='TABLE-NIZA', quantity=10, eta=date.today())


@pytest.fixture
def make_batch(batch):
    def _make_batch(eta) -> Batch:
        b = copy.copy(batch)
        b.eta = eta
        return b

    return _make_batch


@pytest.fixture
def order(customer):
    return Order('ORDER-REFERENCE', customer, [])


@pytest.fixture
def line(order):
    return OrderLine('TABLE-NIZA', 5, order)


@pytest.fixture
def customer():
    return Customer()