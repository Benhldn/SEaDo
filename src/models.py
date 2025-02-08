from .database import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean


class User(Base, UserMixin):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), unique=False, nullable=False)
    admin = Column(Boolean, unique=False, nullable=True)
    

class Ticket(Base):
    __tablename__='ticket'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=False, nullable=True)
    title = Column(String(800), unique=False, nullable=False)
    description = Column(String(8000), unique=False, nullable=False)
    date = Column(String(800), unique=False, nullable=False)