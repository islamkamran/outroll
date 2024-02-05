from fastapi import HTTPException
from jose import jwt, JWTError
import json

SECRET_KEY = "38df3dec89825167e6a6a72586abe08560a60d407149076d330a0b310ecb75bc"  # Use a secure, secret value
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
