
from typing import List

from sqlalchemy.orm import Session, joinedload, selectinload

import models
from custom_exceptions.not_found_exception import NotFoundException
from dtos.items import CreateItemCopyReq, CreateItemReq
from services.abc_item_service import ABCItemService
from custom_exceptions.business_rule_exception import BusinessRuleException

class ItemService(ABCItemService):

    def __init__(self, _repository: Session):
        self._repository = _repository

    def get_all(self) -> List[models.Item]:
        return (self._repository.query(models.Item)
                # joinedload: yksi kysely, jossa on JOIN.
                # Hyvä monta-yhteen-suuntaan (nimikkeellä on yksi kategoria).
                .options(joinedload(models.Item.category))
                # selectinload: toinen kysely, jossa WHERE id IN (...).
                # Parempi yksi-moneen-suuntaan, koska JOIN monistaisi rivejä.
                .options(selectinload(models.Item.copies))
                .all())

    def get_by_id(self, _id: int) -> models.Item:
        item = (self._repository.query(models.Item)
                .options(joinedload(models.Item.category))
                .options(selectinload(models.Item.copies))
                .filter_by(id=_id)
                .first())

        if item is None:
            raise NotFoundException(f'item {_id} not found')

        return item

    def create(self, req: CreateItemReq) -> models.Item:
        # Viiteavaimen pitää osoittaa olemassa olevaan kategoriaan.
        # Ilman tätä tarkistusta tietokanta heittäisi viiteavainvirheen, josta tulisi 500.
        category = self._repository.query(models.Category).filter_by(id=req.category_id).first()
        if category is None:
            raise NotFoundException(f'category {req.category_id} not found')

        item = models.Item(name=req.name, description=req.description, category_id=req.category_id)
        self._repository.add(item)
        self._repository.commit()

        # Haetaan tallennettu nimike uudelleen, jotta kategoria ja kappaleet tulevat mukaan
        return self.get_by_id(item.id)

    def add_copy(self, item_id: int, req: CreateItemCopyReq) -> models.ItemCopy:
        # Nimikkeen pitää olla olemassa. get_by_id nostaa NotFoundExceptionin, jos ei ole.
        self.get_by_id(item_id)

        # Inventaarionumero on yksilöllinen, samoin kuin kategorian nimi
        code_taken = (self._repository.query(models.ItemCopy)
                    .filter_by(inventory_code=req.inventory_code)
                    .first() is not None)

        if code_taken:
            raise BusinessRuleException(f'inventory code {req.inventory_code} already exists')

        copy = models.ItemCopy(inventory_code=req.inventory_code, item_id=item_id)
        self._repository.add(copy)
        self._repository.commit()

        return copy