from sqlalchemy.orm import Session
from app.db.models import User, RollOutBillBoard, BookBillBoard
from app.db.schemas import ForgotPassword
import logging
from sqlalchemy import or_


def create_user(db: Session, user_data):
    new_user = User(**user_data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logging.info(f'new user registered in DB with the id: {new_user.id}')
    return new_user


async def get_user_by_credentials(db: Session, phonenumber: str):
    user_record = db.query(User).filter(User.phonenumber == phonenumber).first()
    logging.info(f'the user record found in DB: {user_record}')
    return user_record


async def get_user_by_google_credentials(db: Session, user_data):
    user_record = db.query(User).filter(User.email == user_data.email).first()
    logging.info(f'the google-user record found in DB: {user_record}')
    return user_record


def get_forgot_password(db: Session, user_data: ForgotPassword):
    if user_data.phonenumber:
        return db.query(User).filter(User.phonenumber == user_data.phonenumber).first()
    elif user_data.email:
        return db.query(User).filter(User.email == user_data.email).first()
    return None


# **************** BillBoards *************************

def list_record(db: Session):
    logging.info('Taking all the Billboards data in crud operations which is accessing RollOutBillBoards table')
    return db.query(RollOutBillBoard).all()


def my_billboards(db: Session, user_id):
    return db.query(RollOutBillBoard).filter(RollOutBillBoard.fk_user_id == user_id).all()


def my_booked_billboards(db: Session, user_id):
    logging.info('returning my booked billboards from crud funtion my_booked_billboards which is accessing BookBillBoard table')
    return db.query(BookBillBoard).filter(BookBillBoard.fk_user_id == user_id).all()


def rollout_billboard(db: Session, user_data):
    new_billboard = RollOutBillBoard(**user_data.dict())
    logging.info('RolloutBillBoard table is recieving data from crud rollout_billboard')

    db.add(new_billboard)
    db.commit()
    db.refresh(new_billboard)
    return new_billboard.rolloutid


def book_billboard(db: Session, user_data):
    book_new_billboard = BookBillBoard(**user_data.dict())
    #filter here for checking if billboard is avaliable or not
    db.add(book_new_billboard)
    db.commit()
    db.refresh(book_new_billboard)
    print(f'the id: {book_new_billboard.bookingbillboardid}')
    return book_new_billboard.bookingbillboardid


def search_billboards(db: Session, place):
    # return db.query(RollOutBillBoard).filter(RollOutBillBoard).all()
    print(f'in DB crud operations: {place}')
    return db.query(RollOutBillBoard).filter(or_(*[RollOutBillBoard.location.ilike(f"%{loc}%") for loc in place])).all()
    # return db.query(RollOutBillBoard).all()
