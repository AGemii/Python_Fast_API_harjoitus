
from pydantic import BaseModel, ConfigDict, Field


class CategoryDto(BaseModel):
    # from_attributes sallii luonnin suoraan SQLAlchemy-oliosta
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CreateCategoryReq(BaseModel):
    # Pydantic validoi nämä automaattisesti.
    # min_length ja max_length vastaavat C#:n DataAnnotations-attribuutteja.
    name: str = Field(min_length=2, max_length=50)