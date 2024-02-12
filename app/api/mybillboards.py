from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import my_billboards
from app.helper.jwt_token_decode import decode_token


router = APIRouter()


@router.get("/v1/mybillboards")
def myrollouts(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    user_id = decode_token(token)  # Extracting the user_id as it would be used as foreign Key in the rollout table
    print(f'the user id after decoding: {user_id}')
    try:
        return {"My Published Rollouts": my_billboards(db, user_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    # retval = {
    #     # "rollout_id": rollout_id
    # }

    # return {"Message": "Successfull", "Billboard Rolled Out": retval}
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


