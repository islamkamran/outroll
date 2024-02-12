from fastapi import HTTPException
from jose import jwt, JWTError
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        sub_dict = json.loads(sub.replace("'", '"'))
        user_id = sub_dict.get("userid")
        print(f'the user ID extracted from token in decode: {user_id}')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token missing user ID")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
