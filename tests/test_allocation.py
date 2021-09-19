from model.model import *
from datetime import timedelta
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_warehouse_batches_to_shipments(make_batch, line):
    batch_warehouse = make_batch(eta=None)
    batch_shipment = make_batch(eta=today)
    batch_warehouse_2 = make_batch(eta=None)
    batches = [batch_warehouse, batch_shipment, batch_warehouse_2]
    assert batch_warehouse.reference == allocate(line, batches)


def test_prefers_earlier_batches(make_batch, line):
    batch_shipment_tomorrow = make_batch(eta=tomorrow)
    batch_shipment_later = make_batch(eta=later)
    batches = [batch_shipment_tomorrow, batch_shipment_later]
    assert batch_shipment_tomorrow.reference == allocate(line, batches)


def test_out_of_stock(batch, order):
    with pytest.raises(OutOfStock):
        line = OrderLine('SKU-001', 100, order)
        allocate(line, [batch])
