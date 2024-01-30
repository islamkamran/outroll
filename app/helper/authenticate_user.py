from fastapi import HTTPException
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#def authenticate_user(user record from DB, user data input from user)


def autheticate_user(user_record, user_data):
    # I am fetching password directly check it out
    # print(f'user_record inside authenticate_user: {user_record.password}')
    # print(f'user_data inside authenticate_user: {user_data}')
    try:
        print("here 1")
        # remember the sequence of decrypting of matters !!!!!!!!
        if verify_password(user_data.password, user_record.password):
            print("2")
            retval = {
                "userid": user_record.id,
                "username": user_record.fullname,
                "phonenumber": user_record.phonenumber,
                "email": user_record.email
            }
            print(retval)
            print("3")
            return {"Message": retval}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
