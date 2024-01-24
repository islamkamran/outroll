from app.db.database import user_database
from app.db.database import user_database
# from app.db.

async def create_user(fullname: str, phonenumber: str, email: str, password: str):
    query = """
    INSERT INTO users(fullname, phonenumber, email, password)
    VALUES(:fullname, :phonenumber, :email, :password)
    """
    values = {"fullname": fullname, "phonenumber": phonenumber, "email": email, "password": password}
    user_id = await user_database.execute(query, values)
    return user_id

async def get_user_by_credentials(query:str,values:dict):
    user_record = await user_database.fetch_one(query,values)
    return user_record

async def get_user_by_id(query:str,values:dict):
    user_record = await user_database.fetch_one(query,values)
    return user_record

async def get_userlogin_by_credentials(query:str,values:dict):
    user_record = await user_database.fetch_one(query,values)
    return user_record

async def get_forgot_password(query:str,values:dict):
    user_record = await user_database.fetch_one(query,values)
    return user_record

# **************** BillBoards *************************
async def rollout_billbaord(location:str, price:str, size:str, status:str,register_date:str,picture:str,fk_user_id:int):
    query = """
    INSERT INTO rolloutbillboard(location,price,size,status,register_date,picture,fk_user_id)
    VALUES(:location,:price,:size,:status,:register_date,:picture,:fk_user_id)
    """
    values = {"location":location,"price":price,"size":size,"status":status,"register_date":register_date,"picture":picture,"fk_user_id":fk_user_id}
    rollout_id = await user_database.execute(query,values)
    return rollout_id