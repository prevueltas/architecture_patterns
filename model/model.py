from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


class OutOfStock(Exception):
    pass


class NotEnoughStock(Exception):
    pass


class DuplicatedOrderLine(Exception):
    pass


class LineNotFound(Exception):
    pass


class Customer:
    pass


@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int

    def __repr__(self):
        return f"<OrderLine {self.sku} of Order {self.order_id}>"


@dataclass
class Order:
    reference: str
    customer: Customer
    lines: [OrderLine]

    def __repr__(self):
        return f"<Order {self.reference}>"


class Batch:
    def __init__(self, reference: str, sku: str, purchased_qty: int, eta: Optional[date] = None):
        self.reference = reference
        self.sku = sku
        self._purchased_qty = purchased_qty
        self.eta = eta
        self._lines = set()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        else:
            return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        elif other.eta is None:
            return True
        return self.eta > other.eta

    def __repr__(self):
        return f"<Batch {self.reference}>"

    @property
    def available_qty(self):
        return self._purchased_qty - sum([line.qty for line in self._lines])

    def can_allocate(self, line: OrderLine) -> bool:
        if self.sku == line.sku and self.available_qty >= line.qty:
            return True
        else:
            return False

    def allocate(self, line: OrderLine):
        if self.available_qty < line.qty:
            raise NotEnoughStock(
                f"There is not enough stock in this {self} to serve the OrderLine {line}")
        else:
            if line in self._lines:
                raise DuplicatedOrderLine(f"Duplicated OrderLine {line} in {self}")
            self._lines.add(line)

    def deallocate(self, line: OrderLine):
        try:
            self._lines.remove(line)
        except KeyError:
            raise LineNotFound


def allocate(line: OrderLine, batches: [Batch]) -> str:
    for batch in sorted(batches):
        if batch.can_allocate(line):
            batch.allocate(line)
            return batch.reference
    raise OutOfStock(f"Out of Stock for sku {line.sku}")

# def cool_allocate(line: Line, batches: [Batch]) -> str:
#     try:
#         batch = next(b for b in sorted(batches) if b.sku == line.sku and b.can_allocate)
#         batch.allocate(line)
#         return batch.reference
#     except StopIteration:
#         raise OutOfStock(f"Out of Stock for sku {line.sku}")
