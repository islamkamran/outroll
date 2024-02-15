from fastapi import APIRouter, HTTPException, Depends
from app.db.crud import get_user_by_credentials, get_user_by_google_credentials, create_user
from app.helper.authenticate_user import autheticate_user
from app.db.schemas import User, Signin, SigninWithGoogle
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.helper.jwt_token import jwt_access_token
import logging


router = APIRouter()
# Signin API for entering into the application


@router.post("/v1/user/signin")
async def signin(user_data: Signin, db: Session = Depends(get_db)):
    user_record = await get_user_by_credentials(db, user_data.phonenumber)
    logging.info('Finding if user record exist in DB')
    if user_record is None:
        logging.error(f'Error user not found: {user_record}')
        raise HTTPException(status_code=404, detail="User not found")
    try:
        logging.info('checking the user credentials if correct than access will be given')
        return autheticate_user(user_record, user_data)
    except Exception as e:
        logging.error(f'Error occured in signin: {str(e)}')
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/v1/user/signin_with_google")
async def signin_with_google(user_data: SigninWithGoogle, db: Session = Depends(get_db)):
    try:
        user_record = await get_user_by_google_credentials(db, user_data)
        if user_record is not None:
            logging.info('user record already in database by email')
            retval = {
                "userid": user_record.id,
                "full name": user_record.fullname,
                "email": user_record.email
            }
        else:
            new_user = create_user(db, User(**user_data.dict()))
            logging.info('user with google id is not in DB registering the user and then will be outputing the data')
            try:
                user_record = await get_user_by_google_credentials(db, new_user)
                logging.info('Registering the new user in DB with google login')
                retval = {
                    "userid": user_record.id,
                    "full name": user_record.fullname,
                    "email": user_record.email
                }
            except Exception as e:
                logging.error(f'Error occured in new registeration and login with google: {str(e)}')
                raise HTTPException(status_code=404, detail=str(e))
        return {"access_token": jwt_access_token(retval), "token_type": "bearer"}
    except Exception as e:
        logging.error(f'Error occured in login with google api: {str(e)}')
        raise HTTPException(status_code=400, detail=str(e))
