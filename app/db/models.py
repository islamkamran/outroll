from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
from app.db.db_setup import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    fullname = Column(String(255), index=True, nullable=False)
    phonenumber = Column(String(15), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=True)


class RollOutBillBoard(Base):
    __tablename__ = "rolloutbillboard"
    rolloutid = Column(Integer, primary_key=True, index=True, nullable=False)
    location = Column(String(255), index=True, nullable=False)
    price = Column(String(255), index=True, nullable=False)
    length = Column(String(255), index=True, nullable=False)
    width = Column(String(255), index=True, nullable=False)
    measurement_unit = Column(String(255), index=True, nullable=False)  # This line is for checking if the measurement will be in inches, foots or meters
    type = Column(String(255), index=True, nullable=False) # This line show the type of the billboard
    installation = Column(String(255), index=True, nullable=False) # This line is for checking if the owner provides installation or not
    status = Column(String(255), index=True, nullable=False)
    register_date = Column(String(255), nullable=False)
    picture = Column(String(255), index=True, nullable=False)

    fk_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class BookBillBoard(Base):
    __tablename__ = "bookbillboard"
    bookingbillboardid = Column(Integer, primary_key=True, index=True, nullable=False)
    booking_status = Column(String(255), index=True, nullable=False)
    booking_date_from = Column(String(255), index=True, nullable=False)
    booking_date_to = Column(String(255), index=True, nullable=False)
    total_days = Column(Integer, index=True, nullable=False)

    rollout_id = Column(Integer, ForeignKey("rolloutbillboard.rolloutid"), nullable=False)
    fk_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
