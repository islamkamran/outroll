from fastapi import HTTPException
from passlib.context import CryptContext
from app.helper.jwt_token import jwt_access_token, jwt_refresh_token
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def autheticate_user(user_record, user_data):
    # I am fetching password directly check it out
    # print(f'user_record inside authenticate_user: {user_record.password}')
    # print(f'user_data inside authenticate_user: {user_data}')
    try:
        # remember the sequence of decrypting of matters !!!!!!!!
        if not verify_password(user_data.password, user_record.password):
            logging.error('Error occured in authenticating the credentials of the user')
            raise HTTPException(status_code=400, detail="password/phonenumber")

        retval = {
            "userid": user_record.id,
            "username": user_record.fullname,
            "phonenumber": user_record.phonenumber,
            "email": user_record.email
        }
        logging.debug('making the token and refresh token')
        return {"access_token": jwt_access_token(retval), "token_type": "bearer", "refresh_token": jwt_refresh_token(retval)}
    except Exception as e:
        logging.error('Error occured in authenticate_user')
        return {"error": str(e)}
