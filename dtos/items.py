
from pydantic import BaseModel, ConfigDict, Field


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


# lisää tiedoston alkuun: from pydantic import ConfigDict

class CreateItemCopyReq(BaseModel):
    # Inventaarionumero, esim. "CAM-001"
    inventory_code: str = Field(min_length=1, max_length=50)


class ItemCopyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventory_code: str
    item_id: int