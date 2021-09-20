import pytest
from datetime import date
from model.model import OrderLine
from repository.repository import BatchesSqlRepository, NoResultFound


def test_repository_can_save_a_batch(session, batch):
    batch_repository = BatchesSqlRepository(session)
    batch_repository.add(batch)


def test_repository_can_get_a_batch(session, batch):
    batch_repository = BatchesSqlRepository(session)
    batch_repository.add(batch)
    batch_saved = batch_repository.get(batch.reference)
    assert batch_saved.reference == batch.reference


def test_repository_raise_exception_if_batch_doesnt_exist(session, batch):
    batch_repository = BatchesSqlRepository(session)
    with pytest.raises(NoResultFound):
        batch_repository.get('SOMEREF')


def test_repository_can_list_batches(session, make_batch):
    batch_repository = BatchesSqlRepository(session)
    batch_repository.add(make_batch(eta=date.today()))
    batch2 = make_batch(eta=None)
    # Batches with same reference are considered equal, hence we change it so it can be added to the set type
    batch2.reference = 'REF8347466'
    batch_repository.add(batch2)
    rows = batch_repository.list()
    assert len(rows) == 2
    assert rows[1].reference == batch2.reference


def test_repository_can_get_a_line_from_its_batch(session, batch):
    batch_repository = BatchesSqlRepository(session)
    line = OrderLine('ORDER_ID', batch.sku, 1)
    session.add(line)
    batch.allocate(line)
    batch_repository.add(batch)
    batch_saved = batch_repository.get(batch.reference)
    assert batch_saved._lines == {line}
