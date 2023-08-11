"""Создать RESTful API для управления списком задач.
Каждая задача должна содержать следующие поля: ID (целое число),
Название (строка), Описание (строка), Статус (строка): "to do", "in progress", "done".
Приложение должно использовать FastAPI и поддерживать следующие функции:
Создайте функцию get_tasks для получения списка всех задач (метод GET).
Создайте функцию get_task для получения информации о задаче по её ID
(метод GET).
Создайте функцию create_task для добавления новой задачи (метод POST).
Создайте функцию update_task для обновления информации о задаче по её ID
(метод PUT).
Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Literal

from list_task import ListTasks, TaskInList

app = FastAPI()


class Task(BaseModel):
    name: str
    description: str
    status: Literal["todo", "in progress", "done"]


tasks = ListTasks([
    Task(name='NewTask', description='Some description for task', status='in progress'),
    Task(name='NewTask', description='Some description for task', status='to do'),
    Task(name='NewTask', description='Some description for task', status='done'),
])


@app.get('/tasks/', summary='Get all tasks')
async def get_tasks() -> list[TaskInList]:
    return tasks.get_tasks()


@app.get('/tasks/{task_id}/', summary='Get tasks by ID')
async def get_tasks(task_id: int) -> TaskInList:
    return tasks.get_task(task_id)


@app.post('/tasks/', summary='Add task in list of the tasks')
async def create_task(task: Task) -> None:
    tasks.add_task(task)


@app.put('/tasks/{tasks_id}/', summary='Change task in list of tasks')
async def update_task(tasks_id: int, task: Task) -> None:
    tasks.change_task(tasks_id, task)


@app.delete('/tasks/{tasks_id}/', summary='Delete task from list of tasks')
async def delete_task(tasks_id: int) -> None:
    tasks.delete_task(tasks_id)


if __name__ == '__main__':
    uvicorn.run('tasks:app', reload=True)
