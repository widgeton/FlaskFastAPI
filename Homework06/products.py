from fastapi import APIRouter, Path

from db import db, products
from models import Product, ProductIn

router = APIRouter()


@router.get('/products/', response_model=list[Product])
async def get_products():
    query = products.select()
    return await db.fetch_all(query)


@router.get('/products/{product_id}/', response_model=Product)
async def get_product(product_id: int = Path(..., ge=0, title='ID', description='The ID of the product')):
    query = products.select().where(products.c.id == product_id)
    return await db.fetch_one(query)


@router.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(title=product.title, description=product.description, price=product.price)
    last_record_id = await db.execute(query)
    return Product(id=last_record_id, **product.model_dump())


@router.put('/products/{product_id}/', response_model=Product)
async def update_product(new_product: ProductIn, product_id: int = Path(..., ge=0, title='ID',
                                                                        description='The ID of the product')):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await db.execute(query)
    return Product(id=product_id, **new_product.model_dump())


@router.delete('/products/{product_id}/', response_model=dict)
async def delete_product(product_id: int = Path(..., ge=0, title='ID', description='The ID of the product')):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {'message': 'User was deleted successfully'}
