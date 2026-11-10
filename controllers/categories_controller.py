
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from custom_exceptions.business_rule_exception import BusinessRuleException
import dtos.categories
from custom_exceptions.not_found_exception import NotFoundException
from factories.services import category_service_factory
from services.abc_category_service import ABCCategoryService

router = APIRouter(prefix='/api/categories', tags=['categories'])

# Typealias, jotta Dependsiä ei tarvitse toistaa joka handlerissa.
# Tyyppinä on abstrakti base-luokka, joten mikä tahansa sen perivä
# konkreettinen service kelpaa (polymorfismi).
CategoryServ = Annotated[ABCCategoryService, Depends(category_service_factory)]


@router.get('/')
def get_all(_service: CategoryServ) -> List[dtos.categories.CategoryDto]:
    return _service.get_all()


@router.get('/{category_id}')
def get_by_id(category_id: int, _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return _service.get_by_id(category_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return _service.create(req)
    except BusinessRuleException as error:
        raise HTTPException(status_code=409, detail=str(error))

@router.put('/{category_id}')
def update(category_id: int, req: dtos.categories.CreateCategoryReq,
           _service: CategoryServ) -> dtos.categories.CategoryDto:
    try:
        return _service.update(category_id, req)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except BusinessRuleException as error:
        raise HTTPException(status_code=409, detail=str(error))



@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(category_id: int, _service: CategoryServ):
    try:
        _service.delete(category_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    # tämä on uusi
    except BusinessRuleException as error:
        # 409 Conflict: pyyntö oli kelvollinen, mutta se on ristiriidassa
        # resurssin nykytilan kanssa
        raise HTTPException(status_code=409, detail=str(error))