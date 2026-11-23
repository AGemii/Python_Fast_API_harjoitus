
from pydantic import BaseModel, ConfigDict
from typing import Literal

class UserDto(BaseModel):
    # from_attributes sallii luonnin suoraan SQLAlchemy-oliosta,
    # eli Pydantic lukee kentät model-olion attribuuteista
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str

class SetRoleReq(BaseModel):
    # Literal hylkää muut arvot jo validoinnissa (422)
    role: Literal['user', 'staff', 'admin']