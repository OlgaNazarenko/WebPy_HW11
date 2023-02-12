from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'sqlite:///mycontact.db'
engine = create_engine(DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
