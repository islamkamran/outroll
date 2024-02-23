from fastapi import APIRouter, HTTPException, Depends, Form
from app.db.crud import search_billboards
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
import logging

router = APIRouter()


@router.get("/v1/searchbillboard")
def search_list(place: str = Form(...), db: Session = Depends(get_db)):
    try:
        place = place.replace(" ", "")  # remove the spaces 
        place = place.split(',')  # This become a list
        return {"List": search_billboards(db, place)}
    except Exception as e:
        logging.error(f'Error occured in listbillboards api; {str(e)}')
        raise HTTPException(status_code=400, detail=f"{e}")
