
import abc
from typing import List

import models
from dtos.items import CreateItemCopyReq, CreateItemReq


class ABCItemService(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> List[models.Item]:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def get_by_id(self, _id: int) -> models.Item:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def create(self, req: CreateItemReq) -> models.Item:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def add_copy(self, item_id: int, req: CreateItemCopyReq) -> models.ItemCopy:
        raise NotImplementedError()  # pragma: no cover