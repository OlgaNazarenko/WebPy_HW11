from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    surname = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    mobile = Column(Integer, nullable=True)
    date_of_birth = Column(Date)
    user_id = Column('user_id', ForeignKey('users.id',ondelete='CASCADE'), default=None)
    user = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
