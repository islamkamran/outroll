from fastapi import APIRouter,Form, HTTPException
from app.db.crud import create_user,get_user_by_id
from passlib.context import CryptContext
from app.db.models import Signup, Billboard

router = APIRouter()

@router.post("/v1/user/signup")
async def signup(fullname: str = Form(...), phonenumber: str = Form(...), email: str = Form(...), password: str = Form(...),
                  confirm_password: str = Form(...)):
    if(password==""):
         return {"Error": "Password is required"}
    if(confirm_password==""):
         return {"Error": "confirm Password is required"}

    if password != confirm_password:
        return {"Error": "Password do not match"}
    
    # Checking with Pydantic classes
    user = Signup(fullname=fullname,phonenumber=phonenumber,email=email,password=password)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def get_password_hash(password):
        return pwd_context.hash(password)
    
    user.password = get_password_hash(user.password)
    print(user.password)

    user_id = await create_user(user.fullname, user.phonenumber, user.email, user.password)
    if user_id:
        return { "Message": "Register Successful"}
    else:
        raise HTTPException(status_code=400, detail="Registeration failed")
        