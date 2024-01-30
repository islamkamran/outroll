from pydantic import BaseModel, Field


class User(BaseModel):
    fullname: str = Field(min_length=3, max_length=50)
    phonenumber: str = Field(max_length=11)
    email: str = Field(max_length=30)
    password: str = Field(min_length=8)

    class Config:
        orm_mode = True


class Signup(User):
    confirm_password: str = Field(min_length=8)


class Signin(BaseModel):
    phonenumber: str = Field(max_length=11)
    password: str = Field(min_length=8)


class Billboard(BaseModel):
    location: str
    price: int
    size: str
    status: str
    register_date: str
    picture: str
    fk_user_id: str  # may be this part give error remember this in mind
