from fastapi import APIRouter, Path
from hashlib import sha256

from db import users, db
from models import User, UserIn

router = APIRouter()


@router.get('/users/', response_model=list[User])
async def get_users():
    query = users.select()
    return await db.fetch_all(query)


@router.get('/users/{user_id}/', response_model=User)
async def get_user(user_id: int = Path(..., ge=0, title='ID', description='The ID of the user')):
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


@router.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname,
                                  email=user.email, password=sha256(user.password.encode()).hexdigest())
    last_record_id = await db.execute(query)
    return User(id=last_record_id, **user.model_dump())


@router.put('/users/{user_id}/', response_model=User)
async def update_user(new_user: UserIn, user_id: int = Path(..., ge=0, title='ID',
                                                            description='The ID of the user')):
    query = users.update().where(users.c.id == user_id).values(name=new_user.name, surname=new_user.surname,
                                                               email=new_user.email,
                                                               password=sha256(new_user.password.encode()).hexdigest())
    await db.execute(query)
    return User(id=user_id, **new_user.model_dump())


@router.delete('/users/{user_id}/', response_model=dict)
async def delete_user(user_id: int = Path(..., ge=0, title='ID', description='The ID of the user')):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {'message': 'User was deleted successfully'}
