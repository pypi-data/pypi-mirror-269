from pydantic import BaseModel, Field


# User login
class LoginUserRequest(BaseModel):
    user: str = Field(example='johndoe@email.com')
    password: str = Field(example='Pass123')


class RegisterUserRequest(BaseModel):
    fullname: str = Field(example='John Doe')
    username: str = Field(example='john_doe')
    email: str = Field(example='johndoe@email.com')
    password: str = Field(example='Pass123')
    gender: str = Field(example='woman')
    # verification: str = Field(example='...')


class UserAuthResponse(BaseModel):
    access_token: str = Field(example='Bearer ...')
    refresh_access_token: str = Field(example='Bearer ...')
