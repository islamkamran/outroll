from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ********************** JWT Token ************************
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logging.info('JWT token created for the data of the user')
    return encoded_jwt


# ********************** JWT Refresh Token ******************
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(days=7)  # Refresh tokens typically have a longer life
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logging.info('JWT refresh token created for the user data')
    return encoded_jwt


def jwt_access_token(retval):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(retval)}, expires_delta=access_token_expires)
    logging.info('returning the token generated from jwt_access_token() funtion')
    refresh_token = create_refresh_token(data={"sub": str(retval)}, expires_delta=access_token_expires)
    logging.info('returning the refresh token generated from jwt_access_token() funtion')

    return access_token, refresh_token
