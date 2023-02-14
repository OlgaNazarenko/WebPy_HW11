from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Date, DateTime


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    surname = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    mobile = Column(Integer, nullable=True)
    date_of_birth = Column(Date)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
