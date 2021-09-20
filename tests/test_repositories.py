from datetime import date

import pytest
from model.model import Batch
from repository.repository import BatchesFakeRepository


def test_repository_can_save_a_batch(session, batch: Batch):
    batch_repository = BatchesFakeRepository(session)
    batch_repository.add(batch)
    batch_saved = batch_repository.get(batch.reference)
    assert batch_saved.reference == batch.reference


def test_repository_can_get_a_batch(session, batch: Batch):
    batch_repository = BatchesFakeRepository(session)
    batch_repository.add(batch)
    batch_saved = batch_repository.get(batch.reference)
    assert batch_saved.reference == batch.reference


def test_repository_can_list_batches(session, make_batch):
    batch_repository = BatchesFakeRepository(session)
    batch_repository.add(make_batch(eta=date.today()))
    batch2 = make_batch(eta=None)
    # Batches with same reference are considered equal, so we change it so it can be added to the set type
    batch2.reference = 'REF009988'
    batch_repository.add(batch2)
    assert len(batch_repository.list()) == 2
