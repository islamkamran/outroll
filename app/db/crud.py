from sqlalchemy.orm import Session
from app.db.models import User, RollOutBillBoard
from app.db.schemas import ForgotPassword


def create_user(db: Session, user_data):
    new_user = User(**user_data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f'the id: {new_user.id}')
    return new_user


async def get_user_by_credentials(db: Session, phonenumber: str):
    user_record = db.query(User).filter(User.phonenumber == phonenumber).first()
    print(f'the user record found in DB: {user_record}')
    return user_record


async def get_user_by_google_credentials(db: Session, user_data):
    user_record = db.query(User).filter(User.email == user_data.email).first()
    print(f'the google-user record found in DB: {user_record}')
    return user_record


def get_forgot_password(db: Session, user_data: ForgotPassword):
    if user_data.phonenumber:
        return db.query(User).filter(User.phonenumber == user_data.phonenumber).first()
    elif user_data.email:
        return db.query(User).filter(User.email == user_data.email).first()
    return None


# **************** BillBoards *************************

def rollout_billboard(db: Session, user_data):
    new_billboard = RollOutBillBoard(**user_data.dict())

    db.add(new_billboard)
    db.commit()
    db.refresh(new_billboard)
    # print(f'the id: {new_billboard.rolloutid}')
    return new_billboard.rolloutid

# async def rollout_billbaord(location: str, price: str, size: str, status: str,
#                             register_date: str, picture: str, fk_user_id: int):
#     query = """
#     INSERT INTO rolloutbillboard(location,price,size,status,register_date,
#     picture, fk_user_id)
#     VALUES(:location,:price,:size,:status,:register_date,:picture,:fk_user_id)
#     """
#     values = {"location": location, "price": price, "size": size,
#               "status": status, "register_date": register_date,
#               "picture": picture, "fk_user_id": fk_user_id}
#     rollout_id = await user_database.execute(query, values)
#     return rollout_id
