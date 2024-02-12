from fastapi import APIRouter, HTTPException, Depends
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
        raise HTTPException(status_code=500, detail=str(e))
