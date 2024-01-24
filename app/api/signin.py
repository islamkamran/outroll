from fastapi import APIRouter,Form
from app.db.crud import get_user_by_credentials
from fastapi import HTTPException
from app.helper.authenticate_user import autheticate_user


router = APIRouter()
# Signin API for entering into the application 
@router.post("/signin")
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
        
