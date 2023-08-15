import uvicorn
from fastapi import FastAPI

from db import db
import users
import products
import orders

app = FastAPI()
app.include_router(users.router, tags=['users'])
app.include_router(products.router, tags=['products'])
app.include_router(orders.router, tags=['orders'])


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app')
