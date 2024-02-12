from fastapi import APIRouter, HTTPException, Depends
from app.db.crud import get_user_by_credentials, get_user_by_google_credentials, create_user
from app.helper.authenticate_user import autheticate_user
from app.db.schemas import User, Signin, SigninWithGoogle
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.helper.jwt_token import jwt_access_token


router = APIRouter()
# Signin API for entering into the application


@router.post("/v1/user/signin")
async def signin(user_data: Signin, db: Session = Depends(get_db)):
    user_record = await get_user_by_credentials(db, user_data.phonenumber)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        # authenticate_user(data_retrived_from_DB, data_taken_from_user)
        return autheticate_user(user_record, user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/v1/user/signin_with_google")
async def signin_with_google(user_data: SigninWithGoogle, db: Session = Depends(get_db)):
    try:
        user_record = await get_user_by_google_credentials(db, user_data)
        if user_record is not None:
            retval = {
                "userid": user_record.id,
                "full name": user_record.fullname,
                "email": user_record.email
            }
        else:
            new_user = create_user(db, User(**user_data.dict()))
            try:
                user_record = await get_user_by_google_credentials(db, new_user)
                retval = {
                    "userid": user_record.id,
                    "full name": user_record.fullname,
                    "email": user_record.email
                }
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))
        return {"access_token": jwt_access_token(retval), "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
