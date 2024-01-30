from fastapi import APIRouter, Form, HTTPException, Depends
from app.db.crud import get_user_by_credentials
from app.helper.authenticate_user import autheticate_user
from app.db.schemas import Signin, User
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import create_user


router = APIRouter()
# Signin API for entering into the application 
@router.post("/v1/user/signin")
async def signin(user_data: Signin, db: Session = Depends(get_db)):
    user_record = await get_user_by_credentials(db, user_data.phonenumber)
    print(user_record)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # authenticate_user(data_retrived_from_DB, data_taken_from_user)
        return autheticate_user(user_record, user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
# async def signin(phonenumber: str = Form(...), password: str = Form(...)):
    # query = """
    # SELECT * from users
    # WHERE phonenumber = :phonenumber
    # """
    # values = {"phonenumber": phonenumber}
    # user_record = await get_user_by_credentials(query, values)
    # try:
    #     return autheticate_user(user_record, user_data.password)  # called from helper.py
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/v1/user/signin_with_google")
async def signin(fullname: str = Form(...), email: str = Form(...)):
    query = """
    SELECT * from users
    WHERE email = :email
    """
    values = {"email":email}
    user_record = await get_user_by_credentials(query,values)
    try:
        if user_record:
            retval={
                "id":user_record.id,
                "fullname":user_record.fullname,
                "email":user_record.email,
            }
            return retval
        else:
            user_id = await create_user(fullname,None,email,None)
            if user_id:
                query = """
                SELECT * from users
                WHERE email = :email
                """
                values = {"email":email}
                user_record = await get_user_by_credentials(query,values)
                try:
                    if user_record:
                        retval={
                        "id":user_record.id,
                        "fullname":user_record.fullname,
                        "email":user_record.email,
                        }
                except Exception as e:
                    return str(e)
                return retval
            else:
                raise HTTPException(status_code=400, detail="Registeration failed")
            # return retval
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# @router.post("v1/user/signin_with_facebook")
# async def signin(email:str=Form(...)):
#     query = """
#     SELECT * from users
#     WHERE email = :email
#     """
#     values = {"email":email}
#     user_record = await get_user_by_credentials(query,values)
#     try:
#         if user_record:
#             retval={
#                 "id":user_record.id,
#                 "email":user_record.email,
#             }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Data not found")
        
