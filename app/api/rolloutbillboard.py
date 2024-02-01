from fastapi import APIRouter,Form
# from app.db.crud import rollout_billbaord
# from app.db.database import user_database
from fastapi import HTTPException, Header


router = APIRouter()

@router.post("v1/rolloutbillboard")
async def rollout(location:str=Form(...), price:str = Form(...),size:str=Form(...),
                   status:str = Form(...), register_date:str =Form(...),picture:str=Form(...), token:str=Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    fk_user_id = int(token) # Take the token data as JWT token



    rollout_id = await rollout_billbaord(location,price,size,status, register_date,picture,fk_user_id)
    retval = {
        "rollout_id": rollout_id,
        "rollout_location":location,
    }

    return {"Billboard Rolled Out": retval}
    # return rollout_id


