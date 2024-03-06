from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    fullname: str = Field(None, min_length=3, max_length=50)
    phonenumber: str = Field(None, min_length=11, max_length=15)
    email: str = Field(None, max_length=30)
    password: str = Field(None, min_length=8)

    class Config:
        orm_mode = True


class Signup(User):
    confirm_password: str = Field(None, min_length=8)


class Signin(BaseModel):
    phonenumber: str = Field(min_length=11, max_length=15)
    password: str = Field(min_length=8)


class SigninWithGoogle(BaseModel):
    fullname: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=30)


class ForgotPassword(BaseModel):
    phonenumber: Optional[str] = Field(None, min_length=11, max_length=15)
    email: Optional[str] = Field(None, min_length=8)


class Billboard(BaseModel):
    print("in pydantic")
    location: str
    price: int
    length: str
    width: str
    measurement_unit: str
    type: str
    installation: str
    status: str
    register_date: str

    class Config:
        orm_mode = True


class Publish_Billboard(Billboard):
    picture: Optional[str]
    fk_user_id: Optional[int]


class Book_Billboard(BaseModel):
    booking_status: str
    booking_date_from: str
    booking_date_to: str
    total_days: int
    rollout_id: int

    class Config:
        orm_mode = True


class Booking_Done(Book_Billboard):
    fk_user_id: Optional[int]
