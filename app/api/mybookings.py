from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import my_booked_billboards
from app.helper.jwt_token_decode import decode_token
import logging


router = APIRouter()


@router.get("/v1/mybookings")
def mybookings(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        logging.error('The token entered for the user is either wrong or expired')
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    logging.info('token have two parts some time writen as token "value of token" or directly "token"')
        # we have return both the id and the complete data the only purpose is incase of refresh token we need all data in normal case we only need the id as foreign key
    user_id, retval = decode_token(token)  # Extracting the user_id as it would be used as foreign Key in the rollout table
    logging.info(f'the user id after decoding: {user_id}')
    try:
        return {"My Booked Billboards": my_booked_billboards(db, user_id)}
    except Exception as e:
        logging.error(f'Error occured in mybookings api: {str(e)}')
        raise HTTPException(status_code=400, detail=f"{e}")
