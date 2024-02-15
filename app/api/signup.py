from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.db.schemas import Signup, User
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import create_user
import logging

router = APIRouter()


@router.post("/v1/user/signup")
async def signup(user_data: Signup, db: Session = Depends(get_db)):
    logging.info(f'Attempting to register user {user_data.email}')
    try:
        if user_data.password != user_data.confirm_password:
            logging.error('Password and Confirm Password do not match')
            return {"Error": "Password do not match"}

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        def get_password_hash(password):
            return pwd_context.hash(password)

        user_data.password = get_password_hash(user_data.password)

        new_user = create_user(db, User(**user_data.dict()))
        logging.info(f'new user is created {new_user.fullname}')

        if new_user:
            logging.info('User sucessfully added')
            return {"Message": "Register Successful"}
        else:
            raise HTTPException(status_code=400, detail="Registeration failed")
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
