
from pydantic import BaseModel, Field


class ItemDto(BaseModel):
    id: int
    name: str
    description: str | None

    # Nämä kaksi eivät ole Item-modelin attribuutteja, vaan ne lasketaan
    # relaatioista controllerin to_dto-funktiossa (kohta 10).
    # Siksi DTO:ta ei voi luoda suoraan model-oliosta from_attributesilla.

    # Kategorian nimi, ei koko kategoriaoliota
    category_name: str
    copy_count: int


class CreateItemReq(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    # gt=0 varmistaa, että kategorian id on annettu
    category_id: int = Field(gt=0)