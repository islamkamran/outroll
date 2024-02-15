from fastapi import APIRouter, HTTPException, Depends, Header
from app.db.schemas import Book_Billboard, Booking_Done
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import book_billboard
from app.helper.jwt_token_decode import decode_token
import logging


router = APIRouter()


@router.post("/v1/bookbillboard")
def book(user_data: Book_Billboard, authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        logging.error('The token entered for the user is either wrong or expired')
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    logging.info('token have two parts some time writen as token "value of token" or directly "token"')
    user_id = decode_token(token)  # Extracting the user_id as it would be used as foreign Key in the rollout table
    billboard_data = user_data.dict()
    billboard_data["fk_user_id"] = user_id
    booking_id = book_billboard(db, Booking_Done(**billboard_data))
    logging.info(f'Booking done the id is: {booking_id}')
    retval = {
        "booking_id": booking_id
    }

    return {"Message": "Successfull", "Booking Successful": retval}
