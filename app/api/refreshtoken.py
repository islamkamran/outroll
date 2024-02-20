from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.helper.jwt_token_decode import decode_token
from app.helper.jwt_token import jwt_access_token
import logging


router = APIRouter()
# Refresh API for entering into the application


@router.post("/v1/user/refreshtoken")
async def refresh_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    # Verify refresh token and extract user ID
    try:
        if authorization is None:
            logging.error('The token entered for the user is either wrong or expired')
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        logging.info('token have two parts some time writen as token "value of token" or directly "token"')
        # we have return both the id and the complete data the only purpose is incase of refresh token we need all data in normal case we only need the id as foreign key
        user_id, retval = decode_token(token)
        logging.debug("decoding the refresh token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Optionally, check if the user still exists and is active

    # Generate a new access token
    logging.info('new token generated in refresh api')
    return {"access_token": jwt_access_token(retval), "token_type": "bearer"}
