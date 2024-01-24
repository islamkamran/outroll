from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


# #*********STEP#1 : CREATE ENGINE**********
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()




from databases import Database

DATABASE_URL = "sqlite:///./users.db"
user_database = Database(DATABASE_URL)

async def connect_db():
    await user_database.connect()

async def disconnect_db():
    await user_database.disconnect()

async def create_tables():
    queries = [
    """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    phonenumber TEXT,
    email TEXT,
    password TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS rolloutbillboard(
    rolloutid INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    price TEXT,
    size TEXT,
    status TEXT,
    register_date TEXT,
    picture TEXT,
    fk_user_id INTEGER, 
    FOREIGN KEY (fk_user_id) REFERENCES users(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bookbillboards(
    bookingbillboardid INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_status TEXT,
    booking_date_from TEXT,
    booking_date_to TEXT,
    total_days INTEGER
    )
    """
    ]
    for query in queries:
        await user_database.execute(query)
