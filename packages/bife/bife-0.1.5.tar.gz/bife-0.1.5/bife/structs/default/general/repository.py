from typing import Optional

from libs.database import DatabaseHandler
from sqlalchemy import select

from .models import TodoModel
from .schemas import CreateTodoSchema, TodoUpdateSchema


class TodoRepository:

    database_handler = DatabaseHandler()

    def new_todo(self, user_id: int, todo_data: CreateTodoSchema) -> TodoModel:
        with self.database_handler as session:
            todo = TodoModel(user_id=user_id, **todo_data)
            session.add(todo)
            session.expire_on_commit = False
            session.commit()

    def get_todo(self, todo_id: int) -> Optional[TodoModel]:
        with self.database_handler as session:
            query = select(TodoModel.id == todo_id)
            todo = session.scalar(query)
            session.expire_on_commit = False
            session.commit()
            return todo

    def get_all_todos(self) -> list[TodoModel]:
        with self.database_handler as session:
            query = select(TodoModel)
            todo = session.scalars(query).all()
            session.expire_on_commit = False
            session.commit()
            return todo

    def delete_todo(self, todo_id: int) -> Optional[TodoModel]:
        with self.database_handler as session:
            query = select(TodoModel.id == todo_id)
            todo = session.scalar(query)

            session.expire_on_commit = False
            session.commit()
            return todo

    def update_todo(
        self, todo_id: int, todo_new_data: TodoUpdateSchema
    ) -> Optional[TodoModel]:
        with self.database_handler as session:
            query = select(TodoModel.id == todo_id)
            todo = session.scalar(query)
            todo = todo(**todo_new_data)
            session.add(todo)
            session.expire_on_commit = False
            session.commit()
            session.refresh(todo)
            return todo
