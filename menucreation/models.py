from typing import Optional, Any
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float


class Menus(Base):
    __tablename__ = 'menu_list'

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String, unique = True)
    menu_descriptn = Column(String)
    menu_price = Column(Float)
    spicy = Column(Boolean, default=True)
    is_veg = Column(Boolean, default=True)
    menu_type = Column(String)


class Orders(Base):
    __tablename__ = 'placing_orders'

    order_id = Column(Integer, primary_key=True,index=True)
    menu_name = Column(String, ForeignKey("menu_list.menu_name"))
    order_quantitiy = Column(Integer)

