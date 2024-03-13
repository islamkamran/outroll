from fastapi import APIRouter, HTTPException, Depends, Header, File, UploadFile, Form
from app.db.schemas import Billboard, Publish_Billboard
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.crud import rollout_billboard
from app.helper.jwt_token_decode import decode_token
import logging
import os

router = APIRouter()

# Define UPLOAD_DIR here
UPLOAD_DIR = "uploads"


@router.post("/v1/rolloutbillboard")
# def rollout(user_data: Billboard, file: UploadFile = File(...), authorization: str = Header(None), db: Session = Depends(get_db)): # This line was used if we want a direct JSON to be added from from end if we want to add files with json we need Form data the below code is for form data
def rollout(name: str = Form(...), description: str = Form(...), location: str = Form(...), coordinates: str = Form(...), price: int = Form(...), advance_payment: str = Form(...), length: str = Form(...), width: str = Form(...), measurement_unit: str = Form(...), type: str = Form(...), installation: str = Form(...), installation_charges: str = Form(...), status: str = Form(...), register_date: str = Form(), file: UploadFile = File(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    try:
        if authorization is None:
            logging.error('The token entered for the user is either wrong or expired')
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        logging.info('token have two parts some time writen as token "value of token" or directly "token"')

        # we have return both the id and the complete data the only purpose is incase of refresh token we need all data in normal case we only need the id as foreign key
        user_id, retval = decode_token(token)  # Extracting the user_id as it would be used as foreign Key in the rollout table
        logging.info(f'the user id after decoding: {user_id}')

        # checking data through pydantic
        user_data = Billboard(name=name, description=description, location=location, coordinates=coordinates, price=price, advance_payment=advance_payment, length=length, width=width, measurement_unit=measurement_unit, type=type, installation=installation, installation_charges=installation_charges, status=status, register_date=register_date)
        billboard_data = user_data.dict()

        try:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            print(f"Pic uploading error:{e}")
            raise HTTPException(status_code=404, detail=str(e))

        # add image URL
        billboard_data["picture"] = file_path  # this is because we cannot check the files using pydantic we can use but at this stage not required

        # add foreign key
        billboard_data["fk_user_id"] = user_id
        logging.info(f'data: {billboard_data}')

        rollout_id = rollout_billboard(db, Publish_Billboard(**billboard_data))
        retval = {
            "rollout_id": rollout_id
        }

        return {"Message": "Successfull", "Billboard Rolled Out": retval}
    except Exception as e:
        logging.error(f'Error occured while rollouting billboard: {str(e)}')
        raise HTTPException(status_code=409, detail=str(e))
