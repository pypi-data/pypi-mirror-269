from pydantic import BaseModel


class TodoSchema(BaseModel):
    name: str


class CreateTodoSchema(BaseModel):
    name: str


class TodoUpdateSchema(BaseModel):
    name: str
