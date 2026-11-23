
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

import dtos.register, dtos.login

from factories.services import user_service_factory
import models
from services.abc_user_service import ABCUserService
from fastapi import HTTPException
from custom_exceptions.user_registration_exception import UserRegistrationException
from custom_exceptions.not_found_exception import NotFoundException
from typing import List
import dtos.users
from dependencies import get_logged_in_user, require_admin


router = APIRouter(prefix='/api/users', tags=['users'])

# tämä on uusi
UserServ = Annotated[ABCUserService, Depends(user_service_factory)]


# lisää users_controller.py:n alkuun:
# from fastapi import HTTPException
# from custom_exceptions.user_registration_exception import UserRegistrationException

@router.post('/register')
def register(request_data: dtos.register.RegisterReq,
             _user_service: UserServ) -> dtos.register.RegisterRes:
    try:
        user = _user_service.register(request_data.username, request_data.password)
    except UserRegistrationException as error:
        # 409 Conflict: pyyntö oli kelvollinen, mutta käyttäjänimi on jo varattu
        raise HTTPException(status_code=409, detail=str(error))

    return dtos.register.RegisterRes(
        id=user.id,
        username=user.username,
        role=user.role,
    )
@router.post('/login')
def login(request_data: dtos.login.LoginReq, _user_service: UserServ) -> dtos.login.LoginRes:
    try:
        token = _user_service.login(request_data.username, request_data.password)
        return dtos.login.LoginRes(token=token)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Username or password incorrect")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get('/', dependencies=[Depends(require_admin)])
def get_all_users(_user_service: UserServ) -> List[dtos.users.UserDto]:
    try:
        users = _user_service.get_all()

        #return [dtos.users.UserDto.model_validate(user) for user in users]
        return users
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def set_role(self, user_id: int, role: str) -> models.User:
    user = self.get_user_by_id(user_id)

    if user is None:
        raise NotFoundException(f'user {user_id} not found')

    user.role = role
    self._repository.commit()

    return user