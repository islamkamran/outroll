from fastapi import APIRouter,Form
from app.db.crud import get_forgot_password

router = APIRouter()

# Forgot Password API incase the user forgot password
@router.post('/forgotpassword')
async def forgotpassword(username:str=Form(...)):
    query="""
    SELECT * FROM users
    WHERE email = :username OR phonenumber = :username
    """
    values = {"username":username}
    user_record = await get_forgot_password(query,values)
    retval = {
        "Username":user_record.fullname,
        "Password":user_record.password

    }
    if user_record:
        return {"message":retval}
    else:
        return {"Error":"Invalid Phonenumber or Email"}
