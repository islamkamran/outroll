from fastapi import APIRouter, HTTPException, Depends, Query
from app.db.crud import search_billboards
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
import logging

router = APIRouter()


@router.get("/v1/searchbillboard")
def search_list(place: str = Query(None), min_price: str = Query(None), max_price: str = Query(None), type: str = Query(None), db: Session = Depends(get_db)):
    try:
        print(place)
        search_criteria = {}

        if place:
            place_list = place.replace(" ", "").split(',')  # remove the spaces and make it a list
            print(place_list)
            search_criteria['place'] = place_list

        if min_price is not None or max_price is not None:
            search_criteria['price_range'] = (min_price, max_price)

        if type:
            search_criteria['type'] = type
        return {"List": search_billboards(db, search_criteria)}
    except Exception as e:
        logging.error(f'Error occured in listbillboards api; {str(e)}')
        raise HTTPException(status_code=400, detail=f"{e}")
