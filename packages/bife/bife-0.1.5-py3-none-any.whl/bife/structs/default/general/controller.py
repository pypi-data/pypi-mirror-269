from fastapi import APIRouter, Depends
from libs.security.security import Security
from modules.user.models import UserModel

from .repository import TodoRepository
from .schemas import CreateTodoSchema, TodoUpdateSchema

router = APIRouter(prefix='/todo', tags=['todo'])
security = Security()


class TodoController:

    repository: TodoRepository = TodoRepository()

    @router.get('/')
    def get_all_todos(
        self, current_user: UserModel = Depends(security.get_current_user)
    ):
        self.repository.get_all_todos()
        return

    @router.post('/')
    def get_all_todos(
        self, current_user: UserModel = Depends(security.get_current_user)
    ):
        self.repository.new_todo(
            current_user.id,
        )
        return
