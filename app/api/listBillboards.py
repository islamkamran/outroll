from fastapi import APIRouter, HTTPException, Depends
from app.db.crud import list_record
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
import logging

router = APIRouter()


@router.get("/v1/listbillboards")
def list_all(db: Session = Depends(get_db)):
    try:
        return {"List": list_record(db)}
    except Exception as e:
        logging.error(f'Error occured in listbillboards api; {str(e)}')
        raise HTTPException(status_code=400, detail=f"{e}")
