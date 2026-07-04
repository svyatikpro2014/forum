from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Literal


class UserAddSchema(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=5, max_length=72)


class UserResponse(BaseModel):
    id: int
    email: str



class PostAddSchema(BaseModel):
    post_name: str = Field(min_length=1, max_length=30)
    post_topic: Literal["Sports", "Politics", "Games", "News", "Tech", "Other"]
    post_body: str = Field(min_length=1, max_length=1000)



class PostResponse(BaseModel):
    id: int
    post_name: str = Field(min_length=1, max_length=30)
    post_topic: Literal["Sports", "Politics", "Games", "News", "Tech", "Other"]
    post_body: str = Field(min_length=1, max_length=1000)


class PostUpdate(BaseModel):
    post_name: str = Field(min_length=1, max_length=30)
    post_topic: Literal["Sports", "Politics", "Games", "News", "Tech", "Other"]
    post_body: str = Field(min_length=1, max_length=1000)