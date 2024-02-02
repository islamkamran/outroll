from fastapi import APIRouter, HTTPException, Depends, Header
from app.db.schemas import Billboard, Publish_Billboard
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import rollout_billboard
from app.helper.jwt_token_decode import decode_token


router = APIRouter()


@router.post("/v1/rolloutbillboard")
async def rollout(user_data: Billboard, authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print(f'the token from front end: {authorization}')
    print("1")
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    print("2")
    print(token)
    user_id = decode_token(token)
    print(f'the user id after decode: {user_id}')
    billboard_data = user_data.dict()
    billboard_data["fk_user_id"] = user_id
    print(f'Billboard data: {billboard_data}')
    rollout_id = await rollout_billboard(db, Publish_Billboard(**billboard_data))
    retval = {
        "rollout_id": rollout_id
    }

    return {"Message": "Successfull", "Billboard Rolled Out": retval}
    # ******************** the API is done till here use the token ahead *******************
    # fk_user_id = int(token)  # Take the token data as JWT token
    # pr = {
    #     user_data.location,
    #     user_data.price
    # }
    # print(f'user data: {pr}')
    # rollout_id = await rollout_billbaord(location,price,size,status, register_date,picture,fk_user_id)
    # rollout_id = await rollout_billbaord(db, Publish_Billboard(**user_data.dict())) 
    # print(f'the rollout from DB: {rollout_id}')
    

    # return rollout_id


