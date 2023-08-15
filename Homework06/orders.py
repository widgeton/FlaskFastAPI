from fastapi import APIRouter, Path
from sqlalchemy import select
from datetime import date

from db import orders, users, products, db
from models import Order, OrderIn, User, Product

router = APIRouter()


@router.get('/orders/', response_model=list[Order])
async def get_orders():
    query = select(orders.c.id, orders.c.order_date, orders.c.status,
                   products.c.id.label('product_id'), products.c.title, products.c.description, products.c.price,
                   users.c.id.label('user_id'), users.c.name, users.c.surname, users.c.email, users.c.password).join(
        products).join(users)
    rows = await db.fetch_all(query)
    return [Order(id=row.id,
                  order_date=row.order_date,
                  status=row.status,
                  user=User(id=row.user_id,
                            name=row.name,
                            surname=row.surname,
                            password=row.password,
                            email=row.email),
                  product=Product(id=row.product_id,
                                  title=row.title,
                                  description=row.description,
                                  price=row.price)) for row in rows]


@router.get('/orders/{orders_id}/', response_model=Order)
async def get_order(order_id: int):
    order = await db.fetch_one(orders.select().where(orders.c.id == order_id))
    user = await db.fetch_one(users.select().where(users.c.id == order.user_id))
    user = User(id=user.id, name=user.name, surname=user.surname, email=user.email, password=user.password)
    product = await db.fetch_one(products.select().where(products.c.id == order.product_id))
    product = Product(id=product.id, title=product.title, description=product.description, price=product.price)
    return Order(product=product, user=user, id=order.id, order_date=order.order_date, status=order.status)


@router.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id, product_id=order.product_id, status=order.status,
                                   order_date=date.today())
    last_record_id = await db.execute(query)
    return await get_order(last_record_id)


@router.put('/orders/{order_id}/', response_model=Order)
async def update_order(new_order: OrderIn, order_id: int = Path(..., ge=0, title='ID',
                                                                description='The ID of the order')):
    query = orders.update().where(orders.c.id == order_id).values(user_id=new_order.user_id,
                                                                  product_id=new_order.product_id,
                                                                  status=new_order.status,
                                                                  order_date=new_order.order_date)
    await db.execute(query)
    return await get_order(order_id)


@router.delete('/orders/{order_id}/', response_model=dict)
async def delete_order(order_id: int = Path(..., ge=0, title='ID', description='The ID of the order')):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {'message': 'User was deleted successfully'}
