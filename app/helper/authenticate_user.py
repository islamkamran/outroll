from fastapi import HTTPException
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def autheticate_user(user_record,password):
    if user_record == None:
        raise HTTPException(status_code=400, detail="Data not found")
    else:
        try:
            if verify_password(password,user_record.password):  
                retval = {
                    "userid":user_record.id,
                    "username":user_record.fullname,
                    "phonenumber":user_record.phonenumber,
                    "email":user_record.email
                }
                return {"Message":retval} 
            else:
                raise HTTPException(status_code=404, detail="Invalid Parameters")
        except Exception as e:
            raise HTTPException(status_code=400,detail="Data not found")


