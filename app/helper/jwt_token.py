from datetime import datetime, timedelta
from jose import jwt


SECRET_KEY = "38df3dec89825167e6a6a72586abe08560a60d407149076d330a0b310ecb75bc"  # Use a secure, secret value
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def jwt_access_token(retval):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(retval)},
                                       expires_delta=access_token_expires)
    return access_token
