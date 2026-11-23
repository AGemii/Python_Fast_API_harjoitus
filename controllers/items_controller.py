
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

import dtos.items
import models
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.business_rule_exception import BusinessRuleException
from factories.services import item_service_factory
from services.abc_item_service import ABCItemService
from dependencies import get_logged_in_user
from dependencies import require_admin

router = APIRouter(prefix='/api/items', tags=['items'])

ItemServ = Annotated[ABCItemService, Depends(item_service_factory)]


def to_dto(item: models.Item) -> dtos.items.ItemDto:
    # category_name ja copy_count lasketaan relaatioista.
    # Service on ladannut ne valmiiksi, joten tämä ei tee lisäkyselyitä.
    return dtos.items.ItemDto(
        id=item.id,
        name=item.name,
        description=item.description,
        category_name=item.category.name,
        copy_count=len(item.copies),
    )


@router.get('/')
def get_all_items(_item_service: ItemServ) -> List[dtos.items.ItemDto]:
    return [to_dto(item) for item in _item_service.get_all()]


@router.get('/{item_id}')
def get_item_by_id(item_id: int, _item_service: ItemServ) -> dtos.items.ItemDto:
    try:
        return to_dto(_item_service.get_by_id(item_id))
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post('/', status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_logged_in_user)])
def create_item(req: dtos.items.CreateItemReq, _item_service: ItemServ) -> dtos.items.ItemDto:
    try:
        return to_dto(_item_service.create(req))
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.post('/{item_id}/copies', status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_admin)])
def add_copy(item_id: int, req: dtos.items.CreateItemCopyReq,
             _item_service: ItemServ) -> dtos.items.ItemCopyDto:
    try:
        return _item_service.add_copy(item_id, req)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except BusinessRuleException as error:
        raise HTTPException(status_code=409, detail=str(error))