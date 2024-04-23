from pydantic import BaseModel


class CreateTodoSchema(BaseModel):
    name: str


class TodoUpdateSchema(BaseModel):
    name: str
