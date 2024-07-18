from typing import Annotated,List
from fastapi import FastAPI, Body
from typing import Optional, Any
from pydantic import BaseModel
from database import SessionLocal
from models import Menus, Orders
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException
import models
from database import engine
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

session: Session = Depends(get_db)


class MenuList(BaseModel):
    menu_id: int
    menu_name: str 
    menu_descriptn: str
    menu_price: float
    spicy: bool
    is_veg: bool
    menu_type: str

class OrderPlacing(BaseModel):
    order_id: int
    menu_name: str
    order_quantitiy: int

def get_menu_info_by_id(menu_id: int, db: db_dependency ):
    
    """
    Returns the menu based on menu_id
    """

    menu_info = db.query(Menus).get(menu_id)
    return menu_info

def get_order_by_id(order_id: int, db: db_dependency):

    order_info = db.query(Orders).get(order_id)
    return order_info


def update_menu_update(menu_info: MenuList, updatedmenu: MenuList):

    """
    Update the Menu list based on the Menu changes
    """
    menu_info.menu_name = updatedmenu.menu_name
    menu_info.menu_id = updatedmenu.menu_id
    menu_info.menu_descriptn = updatedmenu.menu_descriptn
    menu_info.menu_price = updatedmenu.menu_price
    menu_info.spicy = updatedmenu.spicy
    menu_info.is_veg = updatedmenu.is_veg
    menu_info.menu_type = updatedmenu.menu_type
    return menu_info

def update_orders(order_info: OrderPlacing, updatedorder: OrderPlacing):

    order_info.order_id = updatedorder.order_id
    order_info.order_quantitiy = updatedorder.order_quantitiy
    order_info.menu_name = updatedorder.menu_name

    return order_info



@app.post('/create_menu_list/',status_code=status.HTTP_201_CREATED)
def create_menu_list(menuresponse: MenuList, db: db_dependency):
    """
    This method is able to create new menus onto the Database

    """
    if(db.query(Menus).filter(Orders.order_id == menuresponse.menu_id)):
        raise HTTPException(status_code=404, detail="Menu exists with the ID. You can't create a new Menu rather update the existing Menu")
    menu_list = Menus(**menuresponse.model_dump())
    db.add(menu_list)
    db.commit()
    return(menuresponse)

@app.get('/get_menus_list')
def get_all_menus(db: db_dependency):

    """
    This method is able to get all the menus from the Database

    """
    return db.query(Menus).filter(Menus.menu_id).all()

@app.get('/get_menu_by_id/{menuid}')
def get_menu_by_id(menuid:int, db:db_dependency):
    
    """
    This method is able to get the specific menus from the Database

    """
    fetch_menu = db.query(Menus).filter(Menus.menu_id == menuid).all()
    if not fetch_menu:
        raise HTTPException(status_code=404, detail='Menu not found.')
    
    return db.query(Menus).filter(Menus.menu_id == menuid).all()


@app.put('/update/{menu_id}',status_code=status.HTTP_201_CREATED)
def update_menu(menu_id: int, updatedmenu: MenuList,db: db_dependency):

    """
    This method is able to get update the menus onto the Database

    """
    menu_info = get_menu_info_by_id(menu_id,db)
    print("value")
    print(type(menu_info))
    # menu_info = db.query(Menus).get(menu_id)
    if not menu_info:
        raise HTTPException(status_code=404, detail='Menu not yet available in list to amend the details.')

    menu_update = update_menu_update(menu_info, updatedmenu)
    db.add(menu_update)
    db.commit()
    return(updatedmenu)

@app.delete('/delete_menu/{menu_id}', status_code = status.HTTP_204_NO_CONTENT)
def menu_delete(menu_id: int, db: db_dependency):
    """
    This method is able to delete the menus from the Database

    """
    db.delete(db.query(Menus).get(menu_id))
    db.commit()
    return(db.query(Menus).filter(Menus.menu_id).all())


@app.post('/order_items/',status_code=status.HTTP_201_CREATED)
def orderitems(orderresponse: OrderPlacing, db: db_dependency):
    """
    This method is able to create new orders into the Database

    """
    if(db.query(Orders).filter(Orders.order_id == orderresponse.order_id)):
        raise HTTPException(status_code=404, detail="Already Order Id exist. You can't create a new order rather update the existing order")
    order_list = Orders(**orderresponse.model_dump())
    db.add(order_list)
    db.commit()
    return(orderresponse)


@app.get('/get_all_orders')
def getallorders(db: db_dependency):

    """
    This method is able to get all the orders from the Database

    """
    return db.query(Orders).filter(Orders.order_id).all()

@app.get('/get_by_order_id/{order_id}')
def get_orders_by_id(order_id: int, db: db_dependency):

    """
    Returns the order based on the order id
    """
    order_info = db.query(Orders).get(order_id)  

    return order_info


@app.put('/updateorder/{order_id}',status_code=status.HTTP_201_CREATED)
def updateorders(order_id: int, updatedorder: OrderPlacing,db: db_dependency):

    """
    This method is able to get update the orders into the Database

    """
    order_info = get_order_by_id(order_id,db)
    print("value")
    print(type(order_info))
    # menu_info = db.query(Menus).get(menu_id)
    if not order_info:
        raise HTTPException(status_code=404, detail='Order has not been placed already to amend the orders.')

    order_update = update_orders(order_info, updatedorder)
    db.add(order_update)
    db.commit()
    return(updatedorder)


@app.delete('/delete_the_order/{order_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_the_order_by_id(order_id: int, db: db_dependency):

    """
    This end point will delete the order based on order id
    """

    db.delete(db.query(Orders).get(order_id))
    db.commit()

    return { "message" : f"{order_id} is deleted"}