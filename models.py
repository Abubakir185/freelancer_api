from sqlalchemy import Column, String, Integer, JSON, DateTime, func
from database import Base
import enum
from sqlalchemy import Enum as SqlEnum


class Status(enum.Enum):
    available = "available"
    busy = "busy"
    on_leave = "on_leave"


class Freelancer(Base):
    __tablename__ = 'freelancers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone_number = Column(String)
    age = Column(Integer)
    hashed_password = Column(String, nullable=False)
    skills =  Column(JSON, nullable=False) 
    status = Column(SqlEnum(Status), default="available")

    joined_at = Column(DateTime, default=func.now())

