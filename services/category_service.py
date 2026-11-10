
from typing import List

from sqlalchemy.orm import Session

from custom_exceptions.business_rule_exception import BusinessRuleException
import models
from custom_exceptions.not_found_exception import NotFoundException
from dtos.categories import CreateCategoryReq
from services.abc_category_service import ABCCategoryService


class CategoryService(ABCCategoryService):

    # Session injektoidaan konstruktorissa.
    # Se toimii repositoriona, joten erillistä repository-luokkaa ei tarvita.
    def __init__(self, _repository: Session):
        self._repository = _repository

    def get_all(self) -> List[models.Category]:
        return self._repository.query(models.Category).all()

    def get_by_id(self, _id: int) -> models.Category:
        category = self._repository.query(models.Category).filter_by(id=_id).first()

        if category is None:
            raise NotFoundException(f'category {_id} not found')

        return category

    def create(self, req: CreateCategoryReq) -> models.Category:
        # tämä on uusi
        self._ensure_name_is_free(req.name)

        category = models.Category(name=req.name)

        self._repository.add(category)
        self._repository.commit()

        return category

    def update(self, _id: int, req: CreateCategoryReq) -> models.Category:
        category = self.get_by_id(_id)

        # tämä on uusi. Oma id jätetään pois, jotta nimen voi tallentaa ennallaan.
        self._ensure_name_is_free(req.name, except_id=_id)

        category.name = req.name

        # Huomaa: muokattaessa ei tarvita add-kutsua.
        # SQLAlchemy seuraa hakemaansa oliota ja huomaa muutoksen itse.
        self._repository.commit()

        return category

    def delete(self, _id: int) -> None:
        category = self.get_by_id(_id)
        # Tämä luo kyselyn, joka lopettaa heti ensimmäiseen osumaan.
        # Tehokkaampi kuin hakea kaikki rivit ja laskea niitä.
        has_items = self._repository.query(models.Item).filter_by(category_id=_id).first() is not None

        if has_items:
            raise BusinessRuleException('category cannot be deleted while it has items')
        self._repository.delete(category)
        self._repository.commit()

    # Sama tarkistus tarvitaan kahdessa metodissa, joten se on omassa metodissaan
    def _ensure_name_is_free(self, name: str, except_id: int | None = None) -> None:
        query = self._repository.query(models.Category).filter(models.Category.name == name)
        if except_id is not None:
            query = query.filter(models.Category.id != except_id)

        if query.first() is not None:
            raise BusinessRuleException(f'category {name} already exists')