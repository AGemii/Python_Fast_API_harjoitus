from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unique=True: kahta samannimistä kategoriaa ei ole järkeä olla
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    # Tämä on uusi: yhdellä kategorialla voi olla monta nimikettä
    items: Mapped[List['Item']] = relationship('Item', back_populates='category')

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Viiteavain (foreign key) — tämä on oikeasti tietokannassa sarakkeena
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # relationship EI ole sarake tietokannassa.
    # Se on olemassa vain koodissa, jotta pääset kategoriaan käsiksi nimikkeen kautta.
    category: Mapped['Category'] = relationship('Category', back_populates='items')
    
    # Item-luokkaan
    copies: Mapped[List['ItemCopy']] = relationship('ItemCopy', back_populates='item')


class ItemCopy(Base):
    __tablename__ = 'item_copies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Inventaarionumero, esim. "CAM-001"
    inventory_code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped['Item'] = relationship('Item', back_populates='copies')