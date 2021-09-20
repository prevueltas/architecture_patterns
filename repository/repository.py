import abc
from model.model import Batch


class NotFound(Exception):
    pass


class BatchesAbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: Batch):
        pass

    @abc.abstractmethod
    def get(self, batch_id) -> Batch:
        pass

    @abc.abstractmethod
    def list(self) -> [Batch]:
        pass


class BatchesFakeRepository(BatchesAbstractRepository):
    def __init__(self, session):
        self.session = session
        self._batches = set()

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, batch_id) -> Batch:
        try:
            return next(b for b in self._batches if b.reference == batch_id)
        except StopIteration:
            raise NotFound(f"Batch with id {batch_id} not found")

    def list(self) -> [Batch]:
        return list(self._batches)
