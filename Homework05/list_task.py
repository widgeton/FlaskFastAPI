from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from pydantic import BaseModel
import logging
from typing import Literal

logging.basicConfig(level=logging.INFO, format='%(levelname)s:\t%(msg)s')
logger = logging.getLogger(__name__)


class TaskInList(BaseModel):
    task_id: int
    name: str
    description: str
    status: Literal["todo", "in progress", "done"]


class ListTasks:

    def __init__(self, tasks: list = None):
        self._cursor_id = 1
        self._tasks = []
        if tasks is not None:
            for task in tasks:
                self.add_task(task)

    def get_tasks(self):
        return self._tasks

    def get_task(self, task_id):
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No one task has such ID")

    def add_task(self, task):
        task_in_list = TaskInList(task_id=self._cursor_id, name=task.name,
                                  description=task.description, status=task.status)
        self._tasks.append(task_in_list)
        logger.info(f'Task (ID: {task_in_list.task_id}; Name: {task_in_list.name}) was added successfully')
        self._cursor_id += 1

    def change_task(self, task_id: int, new_task):
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                task_in_list = TaskInList(task_id=self._cursor_id, name=new_task.name,
                                          description=new_task.description, status=new_task.status)
                self._tasks[i] = task_in_list
                logger.info(f'Task (ID: {task_in_list.task_id}; Name: {task_in_list.name}) was changed successfully')
                break
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="No one task has such ID")

    def delete_task(self, task_id: int):
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                logger.info(f'Task (ID: {task.task_id}; Name: {task.name}) was deleted successfully')
                del self._tasks[i]
                break
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="No one task has such ID")
