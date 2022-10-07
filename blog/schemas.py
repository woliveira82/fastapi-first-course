from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class SimpleBlog(Blog):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[SimpleBlog]
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
