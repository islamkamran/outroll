from fastapi import APIRouter,Form
from app.db.crud import get_userlogin_by_credentials

router = APIRouter()
#Login API for logging in into the application if the member is already registered
@router.post("/login")
async def login(username:str=Form(...),password:str=Form(...)):
    query = """
    SELECT * FROM users
    WHERE (phonenumber = :username OR email = :username) AND password = :password
    """
    value = {"username":username,"password":password}
    user_record = await get_userlogin_by_credentials(query,value)
    
    if user_record:
        return {"Message":"Login Successful"}
    else:
        return {"Message":"Invalid Phonenumber or Password"}
