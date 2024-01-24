from fastapi import APIRouter,Form
from app.db.crud import get_user_by_credentials
from fastapi import HTTPException
from app.helper.authenticate_user import autheticate_user
from app.db.crud import create_user,get_user_by_id



router = APIRouter()
# Signin API for entering into the application 
@router.post("/v1/user/signin")
async def signin(phonenumber:str=Form(...),password:str=Form(...)):
    query = """
    SELECT * from users
    WHERE phonenumber = :phonenumber
    """
    values = {"phonenumber":phonenumber}
    user_record = await get_user_by_credentials(query,values)
    try:
        return autheticate_user(user_record,password)# called from helper.py
    except Exception as e:
        raise HTTPException(status_code=400, detail="Data not found")
        
@router.post("/v1/user/signin_with_google")
async def signin(fullname:str = Form(...),email:str=Form(...)):
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
        raise HTTPException(status_code=400, detail="Data not found")
    
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
        
