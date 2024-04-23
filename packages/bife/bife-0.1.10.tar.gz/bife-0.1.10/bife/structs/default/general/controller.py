from fastapi import APIRouter, Depends
from libs.security.security import Security
from modules.user.models import UserModel

from .repository import TodoRepository
from .schemas import CreateTodoSchema, TodoSchema, TodoUpdateSchema

router = APIRouter(prefix='/todo', tags=['todo'])
security = Security()
repository: TodoRepository = TodoRepository()


@router.get('/', response_model=list[TodoSchema])
def get_all_todos(_: UserModel = Depends(security.get_current_user)):
    return repository.get_all_todos()


@router.post('/', response_model=TodoSchema)
def create_todo(
    data: CreateTodoSchema,
    current_user: UserModel = Depends(security.get_current_user),
):
    return repository.new_todo(
        data,
        current_user.id,
    )


@router.get('/{todo_id}', response_model=TodoSchema)
def get_todo_by_id(
    todo_id: int, current_user: UserModel = Depends(security.get_current_user)
):
    return repository.get_todo_by_id(todo_id)


@router.patch('/', response_model=TodoSchema)
def update_todo(
    data: TodoUpdateSchema,
    current_user: UserModel = Depends(security.get_current_user),
):
    return repository.update_todo(
        data.id,
        data,
        current_user.id,
    )


@router.delete('/{todo_id}', response_model=TodoSchema)
def delete_todo(
    todo_id: int, current_user: UserModel = Depends(security.get_current_user)
):
    return repository.delete_todo(
        todo_id,
        current_user.id,
    )
