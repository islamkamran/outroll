# from app.db.database import user_database
# from app.db.
from sqlalchemy.orm import Session
from app.db.models import User, RollOutBillBoard
from app.db.schemas import ForgotPassword


# async def create_user(fullname: str, phonenumber: str, password: str):
def create_user(db: Session, user_data):
    # new_user = User(fullname=user_data.fullname, phonenumber=user_data.phonenumber, password=user_data.password)
    new_user = User(**user_data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f'the id: {new_user.id}')
    return new_user

    # query = """
    # INSERT INTO users(fullname, phonenumber, password)
    # VALUES(:fullname, :phonenumber, :password)
    # """
    # values = {"fullname": fullname, "phonenumber": phonenumber,
    #           "password": password}
    # user_id = await user_database.execute(query, values)
    # return user_id


async def get_user_by_credentials(db: Session, phonenumber: str):
    user_record = db.query(User).filter(User.phonenumber == phonenumber).first()
    print(f'the user record found in DB: {user_record}')
    return user_record
    # await user_database.fetch_one(query, values)


async def get_user_by_google_credentials(db: Session, user_data):
    user_record = db.query(User).filter(User.email == user_data.email).first()
    print(f'the google-user record found in DB: {user_record}')
    return user_record


def get_forgot_password(db: Session, user_data: ForgotPassword):
    print("forgot-1")
    if user_data.phonenumber:
        print("forgot-2")
        return db.query(User).filter(User.phonenumber == user_data.phonenumber).first()
    elif user_data.email:
        print("forgot-3")
        return db.query(User).filter(User.email == user_data.email).first()
    # user_record = await user_database.fetch_one(query, values)
    return None


# async def get_user_by_id(query: str, values: dict):
#     user_record = await user_database.fetch_one(query, values)
#     return user_record


# async def get_userlogin_by_credentials(query: str, values: dict):
#     user_record = await user_database.fetch_one(query, values)
#     return user_record


# **************** BillBoards *************************

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
