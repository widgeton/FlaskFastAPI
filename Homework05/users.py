"""
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для добавления нового пользователя (метод POST).
Создайте маршрут для обновления информации о пользователе (метод PUT).
Создайте маршрут для удаления информации о пользователе (метод DELETE).
Реализуйте валидацию данных запроса и ответа.
Создайте маршрут для отображения списка пользователей (метод GET).
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
import uvicorn

from list_users import ListUsers

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    name: str
    email: str
    password: str


users = ListUsers([
    User(name='John', email='john@gmil.com', password='sdfsdgfhgjhcvb'),
    User(name='Bill', email='bill@gmil.com', password='sdfsdgfhgjhcvb'),
    User(name='Carl', email='carl@gmil.com', password='sdfsdgfhgjhcvb'),
])


@app.get('/', response_class=HTMLResponse, summary='Show users')
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/add_user/', response_class=HTMLResponse, summary='Show form for adding user')
async def add_user_get(request: Request):
    return templates.TemplateResponse('add_user.html', {'request': request})


@app.post('/add_user/', response_class=HTMLResponse, summary='Add user and redirect on main "/"')
async def add_user_post(request: Request):
    form = await request.form()  # нужна библиотека python-multipart
    if form['password'] == form['confirm']:
        users.add_user(User(name=form['name'], email=form['email'], password=form['password']))
        return RedirectResponse('/', status_code=HTTP_302_FOUND)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Password don't match with confirm")


@app.exception_handler(HTTP_401_UNAUTHORIZED)
async def unauthorized_exception(request: Request, ex: HTTPException):
    return templates.TemplateResponse('add_user.html', {'request': request, 'message': ex.detail})


@app.put('/users/{user_id}/', summary='Change user in list of users')
async def change_user(user_id: int, user: User):
    users.change_user(user_id, user)


@app.delete('/users/{user_id}/', summary='Delete user in list of users')
async def delete_user(user_id: int):
    users.delete_user(user_id)


if __name__ == '__main__':
    uvicorn.run('users:app', reload=True)
