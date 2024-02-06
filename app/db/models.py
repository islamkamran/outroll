from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.db_setup import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    fullname = Column(String, index=True, nullable=False)
    phonenumber = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)


class RollOutBillBoard(Base):
    __tablename__ = "rolloutbillboard"
    rolloutid = Column(Integer, primary_key=True, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    price = Column(String, index=True, nullable=False)
    size = Column(String, index=True, nullable=False)
    status = Column(String, index=True, nullable=False)
    register_date = Column(String, nullable=False)
    picture = Column(String, index=True, nullable=False)

    fk_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class BookBillBoard(Base):
    __tablename__ = "bookbillboard"
    bookingbillboardid = Column(Integer, primary_key=True, index=True, nullable=False)
    booking_status = Column(String, index=True, nullable=False)
    booking_date_from = Column(String, index=True, nullable=False)
    booking_date_to = Column(String, index=True, nullable=False)
    total_days = Column(Integer, index=True, nullable=False)
    rollout_id = Column(Integer, ForeignKey("rolloutbillboard.rolloutid"), nullable=False)
    fk_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

