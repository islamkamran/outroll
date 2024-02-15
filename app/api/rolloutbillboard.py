from fastapi import APIRouter, HTTPException, Depends, Header
from app.db.schemas import Billboard, Publish_Billboard
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import rollout_billboard
from app.helper.jwt_token_decode import decode_token
import logging

router = APIRouter()


@router.post("/v1/rolloutbillboard")
def rollout(user_data: Billboard, authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            logging.error('The token entered for the user is either wrong or expired')
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        logging.info('token have two parts some time writen as token "value of token" or directly "token"')

        user_id = decode_token(token)  # Extracting the user_id as it would be used as foreign Key in the rollout table
        logging.info(f'the user id after decoding: {user_id}')
        billboard_data = user_data.dict()
        billboard_data["fk_user_id"] = user_id
        logging.info(f'data: {billboard_data}')
        rollout_id = rollout_billboard(db, Publish_Billboard(**billboard_data))
        retval = {
            "rollout_id": rollout_id
        }
        return {"Message": "Successfull", "Billboard Rolled Out": retval}
    except Exception as e:
        logging.error(f'Error occured while rollouting billboard: {str(e)}')
        raise HTTPException(status_code=409, detail=str(e))
