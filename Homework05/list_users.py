from hashlib import sha256
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:\t%(msg)s')
logger = logging.getLogger(__name__)


class UserInList:
    def __init__(self, user_id: int, name: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = sha256(password.encode()).hexdigest()

    def __repr__(self):
        return f'ID: {self.user_id}; Name: {self.name}'


class ListUsers:

    def __init__(self, users: list = None):
        self._cursor_id = 1
        self._index_cursor = -1
        self._users = []
        if users is not None:
            for user in users:
                self.add_user(user)

    def __iter__(self):
        return self

    def __next__(self):
        self._index_cursor += 1
        if self._index_cursor == len(self._users):
            self._index_cursor = -1
            raise StopIteration
        return self._users[self._index_cursor]

    def add_user(self, user):
        user_in_list = UserInList(user_id=self._cursor_id, name=user.name,
                                  email=user.email, password=user.password)
        self._users.append(user_in_list)
        logger.info(f'User ({user_in_list}) was added successfully')
        self._cursor_id += 1

    def change_user(self, user_id: int, new_user):
        for i, user in enumerate(self._users):
            if user.user_id == user_id:
                user_in_list = UserInList(user_id=user_id, name=new_user.name,
                                          email=new_user.email, password=new_user.password)
                self._users[i] = user_in_list
                logger.info(f'User ({user_in_list}) was changed successfully')
                break
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="No one user has such ID")

    def delete_user(self, user_id: int):
        for i, user in enumerate(self._users):
            if user.user_id == user_id:
                logger.info(f'User ({self._users[i]}) was deleted successfully')
                del self._users[i]
                break
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, detail="No one user has such ID")

    def __repr__(self):
        res = []
        for user in self:
            res.append(str(user))
        return '\n'.join(res)
