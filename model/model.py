from __future__ import annotations

from dataclasses import dataclass
from datetime import date


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


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int
    order: Order

    def __repr__(self):
        return f"<OrderLine {self.sku} of {self.order}>"


@dataclass
class Order:
    reference: str
    customer: Customer
    lines: [OrderLine]

    def __repr__(self):
        return f"<Order {self.reference}>"


class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: date):
        self.reference = reference
        self.sku = sku
        self.purchased_quantity = quantity
        self.eta = eta
        self.lines = []

    def __gt__(self, other):
        if self.eta is None:
            return False
        elif other.eta is None:
            return True
        return self.eta > other.eta

    def __repr__(self):
        return f"<Batch {self.reference}>"

    @property
    def available_quantity(self):
        return self.purchased_quantity - sum([line.quantity for line in self.lines])

    def can_allocate(self, line: OrderLine):
        if self.sku == line.sku and self.available_quantity >= line.quantity:
            return True
        else:
            return False

    def allocate(self, line: OrderLine):
        if self.available_quantity < line.quantity:
            raise NotEnoughStock(
                f"There is not enough stock in this {self} to serve the OrderLine {line}")
        else:
            if line in self.lines:
                raise DuplicatedOrderLine(f"Duplicated OrderLine {line} in {self}")
            self.lines.append(line)

    def deallocate(self, line: OrderLine):
        try:
            self.lines.remove(line)
        except ValueError:
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
