from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from tests.base_model import base_model


class Item(base_model):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    content = Column(String)

    file = relationship("File")


class File(base_model):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    item = Column(ForeignKey(Item.item_id))

    user = relationship("User")


class User(base_model):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    file = Column(ForeignKey(File.id))
    parent_id = Column(ForeignKey("user_account.id"))
    parent = relationship("User", backref="child", remote_side=[id], uselist=True)

    addresses = relationship(
        "Email", back_populates="user", cascade="all,delete-orphan"
    )

    houses = relationship("HouseAssociation", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, parent={self.parent_id})"


class Email(base_model):
    __tablename__ = "email_address"

    address = Column(String, primary_key=True, nullable=False)
    just_field = Column(String, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Email(address={self.address!r})"


class House(base_model):
    __tablename__ = "house"
    name = Column(String, nullable=True)
    label = Column(String, primary_key=True)
    address = Column(String, nullable=True)

    users = relationship("HouseAssociation", back_populates="house")


class HouseAssociation(base_model):
    __tablename__ = "house_association"
    id = Column(Integer, primary_key=True)
    extra = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("user_account.id"))
    house_id = Column(String, ForeignKey("house.label"))

    user = relationship("User", back_populates="houses")
    house = relationship("House", back_populates="users")
