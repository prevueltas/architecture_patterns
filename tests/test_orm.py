from model.model import *


def test_order_line_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (order_id, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order1", "RED-TABLE", 13),
        OrderLine("order2", "BLUE-LIPSTICK", 14)
    ]
    assert session.query(OrderLine).all() == expected
