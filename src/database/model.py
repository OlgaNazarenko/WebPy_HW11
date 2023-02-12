from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Date


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    surname = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    mobile = Column(Integer, nullable=True)
    date_of_birth = Column(Date)
