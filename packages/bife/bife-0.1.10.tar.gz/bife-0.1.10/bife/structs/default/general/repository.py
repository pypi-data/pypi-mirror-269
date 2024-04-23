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
            return todo

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
            todos = session.scalars(query).all()
            session.expire_on_commit = False
            session.commit()
            return todos

    def delete_todo(self, todo_id: int, user_id: int) -> Optional[TodoModel]:
        with self.database_handler as session:
            query = select(TodoModel.id == todo_id)
            todo = session.scalar(query)
            if todo:
                session.delete(todo)
                session.commit()
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
            if todo:
                session.expire_on_commit = False
                for field, value in todo_new_data.items():
                    setattr(todo, field, value)
                session.add(todo)
                session.commit()
                session.refresh(todo)
            return todo
