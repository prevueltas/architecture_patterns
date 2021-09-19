from model.model import *
import pytest


def test_allocating_to_a_batch_reduces_the_available_quantity(batch, line):
    batch.allocate(line)
    assert batch.available_quantity == batch.purchased_quantity - line.quantity


def test_deallocating_to_a_batch_increases_the_available_quantity(batch, line):
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == batch.purchased_quantity


def test_deallocating_a_line_with_does_not_exist(batch, line):
    with pytest.raises(LineNotFound):
        batch.deallocate(line)


def test_can_allocate_if_available_greater_than_required(batch, line):
    batch.allocate(line)


def test_cannot_allocate_if_available_smaller_than_required(batch, order):
    with pytest.raises(NotEnoughStock):
        line = OrderLine('TABLE_NIZA', 11, order)
        batch.allocate(line)


def test_a_batch_cant_allocate_twice_the_same_line(batch, line):
    batch.allocate(line)
    with pytest.raises(DuplicatedOrderLine):
        batch.allocate(line)


def test_can_allocate_if_available_equal_to_required(batch, order):
    line = OrderLine('SKU-001', batch.purchased_quantity, order)
    batch.allocate(line)
