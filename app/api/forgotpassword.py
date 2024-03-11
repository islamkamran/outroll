from fastapi import APIRouter, HTTPException, Depends
from app.db.schemas import ForgotPassword
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import update_password
import logging

router = APIRouter()


@router.post('/v1/user/forgotpassword')
def forgotpassword(user_data: ForgotPassword, db: Session = Depends(get_db)):
    try:
        return update_password(db, user_data)
        # if not user_record:
        #     logging.error('user not found in the DB you are accessing password for wrong user')
        #     raise HTTPException(status_code=404, detail="user not found")
        # else:
        #     logging.info('Records found in DB Now changing the previous record')
        #     retval = update_password(db, user_data)
        #     # retval = {
        #     #     "Username": user_record.fullname,
        #     #     "Password": user_record.password
        #     # }
        #     return {"Message": retval}
    except Exception as e:
        logging.error(f'Error occured in forgotpassword api: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))
