
import abc

import models

from typing import List

class ABCUserService(abc.ABC):
    @abc.abstractmethod
    def register(self, username: str, password:str) -> models.User:
        raise NotImplementedError() # pragma: no cover

    @abc.abstractmethod
    def login(self, username: str, password: str) -> str:
        raise NotImplementedError() # pragma: no cover

    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> models.User | None:
        raise NotImplementedError() # pragma: no cover

    @abc.abstractmethod
    def get_all(self) -> List[models.User]:
        raise NotImplementedError() # pragma: no cover
    
    @abc.abstractmethod
    def get_user_by_access_token(self, access_token: str) -> models.User | None:
        raise NotImplementedError() # pragma: no cover
    
    @abc.abstractmethod
    def set_role(self, user_id: int, role: str) -> models.User:
        raise NotImplementedError()  # pragma: no cover