from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.db.schemas import Signup, User
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import create_user

router = APIRouter()

@router.post("/v1/user/signup")
async def signup(user_data: Signup, db: Session = Depends(get_db)):
    print(user_data)
    if user_data.password != user_data.confirm_password:
        return {"Error": "Password do not match"}
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(password):
        return pwd_context.hash(password)

    user_data.password = get_password_hash(user_data.password)

    new_user = create_user(db, User(**user_data.dict()))
    if new_user:
        return {"Message": "Register Successful"}
    else:
        raise HTTPException(status_code=400, detail="Registeration failed")
