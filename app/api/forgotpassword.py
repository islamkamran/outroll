from fastapi import APIRouter, Form, HTTPException, Depends
from app.db.crud import get_user_by_credentials
from app.helper.authenticate_user import autheticate_user
from app.db.schemas import ForgotPassword
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import get_forgot_password


router = APIRouter()


@router.post('/v1/user/forgotpassword')
def forgotpassword(user_data: ForgotPassword, db: Session = Depends(get_db)):
    try:
        user_record = get_forgot_password(db, user_data)
        if not user_record:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            retval = {
                "Username": user_record.fullname,
                "Password": user_record.password
            }
            return {"Message": retval}
    except Exception as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=500, detail="internal server error")


# Forgot Password API incase the user forgot password
# from fastapi import APIRouter,Form
# from app.db.crud import get_forgot_password



# async def forgotpassword(username:str=Form(...)):
#     query="""
#     SELECT * FROM users
#     WHERE email = :username OR phonenumber = :username
#     """
#     values = {"username":username}
#     user_record = await get_forgot_password(query,values)
#     retval = {
#         "Username":user_record.fullname,
#         "Password":user_record.password

#     }
#     if user_record:
#         return {"message":retval}
#     else:
#         return {"Error":"Invalid Phonenumber or Email"}
