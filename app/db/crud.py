from sqlalchemy.orm import Session
from app.db.models import User, RollOutBillBoard, BookBillBoard
from app.db.schemas import ForgotPassword
import logging
from sqlalchemy import or_, and_
from fastapi import HTTPException


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


def update_billboard(db: Session, rollout_id: int, user_data):
    update_rollout = db.query(RollOutBillBoard).filter(RollOutBillBoard.rolloutid == rollout_id).first()
    if not update_rollout:
        raise HTTPException(status_code=404, detail="Rollout not found")

    # convert the userdata to dict to iterate through it using key value pair
    user_data = user_data.dict()
    for key, value in user_data.items():
        setattr(update_rollout, key, value)

    db.commit()
    return update_rollout.rolloutid


def book_billboard(db: Session, user_data):
    book_new_billboard = BookBillBoard(**user_data.dict())
    #filter here for checking if billboard is avaliable or not
    db.add(book_new_billboard)
    db.commit()
    db.refresh(book_new_billboard)
    print(f'the id: {book_new_billboard.bookingbillboardid}')
    return book_new_billboard.bookingbillboardid


def change_status_message(db: Session, user_data):
    user_data = BookBillBoard(**user_data.dict())
    status_message = db.query(RollOutBillBoard).filter(RollOutBillBoard.fk_user_id==user_data.fk_user_id).first()
    try:
        if status_message:
            status_message.status = user_data.booking_status
            db.commit()
            logging.INFO("status message of the rollout is changed to the user given status")
            return status_message
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def search_billboards(db: Session, search_criteria: dict):
    print("hello2")
    print(search_criteria)
    query = db.query(RollOutBillBoard)

    if 'place' in search_criteria and search_criteria['place']:
        locations_conditions = [RollOutBillBoard.location.ilike(f"%{loc}%") for loc in search_criteria['place']]

        query = query.filter(or_(*locations_conditions))

    if 'price_range' in search_criteria and search_criteria['price_range']:
        min_price, max_price = search_criteria['price_range']
        if min_price is not None and max_price is not None:
            query = query.filter(RollOutBillBoard.price.between(min_price, max_price))
        elif min_price is not None:  # Only min_price provided
            query = query.filter(RollOutBillBoard.price >= min_price)
        elif max_price is not None:  # Only max_price provided
            query = query.filter(RollOutBillBoard.price <= max_price)

    if 'type' in search_criteria and search_criteria['type']:
        query = query.filter(RollOutBillBoard.type == search_criteria['type'])

        # Handle size search
    if 'size_range' in search_criteria and search_criteria['size_range']:
        length, width = search_criteria['size_range']
        if length and width:
            # Example: find billboards where each dimension is within 20% of the requested dimension
            length_lower_bound = float(length) * 0.8
            length_upper_bound = float(length) * 1.2
            width_lower_bound = float(width) * 0.8
            width_upper_bound = float(width) * 1.2
            query = query.filter(
                and_(
                    RollOutBillBoard.length.between(length_lower_bound, length_upper_bound),
                    RollOutBillBoard.width.between(width_lower_bound, width_upper_bound)
                )
            )

    return query.all()


# db.query(RollOutBillBoard).filter(or_(*[RollOutBillBoard.location.ilike(f"%{loc}%") for loc in place])).all()
