import abc
from model.model import Batch


class NoResultFound(Exception):
    pass


class BatchesAbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> [Batch]:
        raise NotImplementedError


class BatchesSqlRepository(BatchesAbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference) -> Batch:
        try:
            return self.session.query(Batch).filter_by(reference=reference).one()
        except Exception:
            raise NoResultFound(f"Batch with reference {reference} not found")

    def list(self) -> [Batch]:
        return self.session.query(Batch).all()
