from __future__ import annotations
from typing import List

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("id_id", ForeignKey("id_table.id"), primary_key=True),
    Column("data_id", ForeignKey("data_table.id"), primary_key=True),
)


class id_table(Base):
    __tablename__ = "id_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    children: Mapped[List[data_table]] = relationship(
        secondary=association_table, back_populates="parents"
    )

    def _init_(self, key, name):
        self.name = name
        self.key = key


class data_table(Base):
    __tablename__ = "data_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[int] = mapped_column()
    users_list: Mapped[str] = mapped_column()
    parents: Mapped[List[id_table]] = relationship(
        secondary=association_table, back_populates="children"
    )

    def __init__(self, key, users_list):
        self.key = key
        self.users_list = users_list

