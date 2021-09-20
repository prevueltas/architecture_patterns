from model.model import *


def test_order_line_mapper_can_save_lines(session, line):
    session.add(line)
    session.commit()


def test_order_line_mapper_can_load_lines(session, line):
    session.add(line)
    session.commit()
    assert [line] == list(session.query(OrderLine).all())


def test_batch_mapper_can_save_batches(session, batch):
    session.add(batch)
    session.commit()


def test_batch_mapper_can_load_batches(session, batch):
    session.add(batch)
    session.commit()
    assert [batch] == list(session.query(Batch).all())


def test_saving_allocation(session, batch, line):
    batch.allocate(line)
    session.add(batch)
    session.commit()
    batch2 = session.query(Batch).filter_by(reference=batch.reference).one()
    assert len(batch2._lines) == 1
