from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func
from sqlalchemy.sql import text

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.database.model import Contact, User
from src.schemas import ContactModel, ContactStatusUpdate


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        id=None,
        name=body.name,
        surname=body.surname,
        email=body.email,
        mobile=body.mobile,
        date_of_birth=body.date_of_birth,
        user_id=user.id
    )
    db.add(contact)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError ("Failed to create user", str(e))
    db.refresh(contact)

    return contact


async def get_contacts(skip: int, limit: int,user: User, db: Session) -> List[Contact]:
    contact = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    return contact


async def get_contact(contact_id: int, user: User,db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id)).first()

    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.mobile = body.mobile
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def get_contacts_choice(name: str | None, surname: str | None,
                              email: str | None, user: User, db: Session):
    contacts = db.query(Contact).filter(and_(or_(
        Contact.name == name, Contact.surname == surname, Contact.email == email),
        Contact.user_id == user.id)
    )

    if name:
        contacts = contacts.filter(Contact.name.like(f"%{name}%"))
    if surname:
        contacts = contacts.filter(Contact.surname.like(f"%{surname}%"))
    if email:
        contacts = contacts.filter(Contact.email.like(f"%{email}%"))
    print(f"name: {name}, surname: {surname}, email: {email}")

    contact = contacts.first()
    return contact


# async def get_contacts_birthdays(user: User, db: Session):
#     seven_days_from_now = datetime.now().date() + timedelta(days=7)
#     contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
#
#     contacts_with_birthdays = [
#         contact for contact in contacts if
#         datetime.now().date().day <= contact.date_of_birth.day < seven_days_from_now.day
#     ]
#
#     return contacts_with_birthdays
#

async def get_contacts_birthdays(user: User, db: Session) :
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days = 7)

    contacts=db.execute(
        text("SELECT * FROM contacts WHERE strftime('%m-%d', date_of_birth) BETWEEN :start_date AND :end_date") ,
        {"start_date" : start_date.strftime("%m-%d") , "end_date" : end_date.strftime("%m-%d")}
    ).fetchall()

    return contacts

    # contacts = db.query(Contact).filter(Contact.user_id == user.id).all()

    # contacts_with_birthdays=[]

    # for contact in contacts :
    #     bday_month = contact.date_of_birth.month
    #     bday_day = contact.date_of_birth.day
    #
    #     # Проверяем, что день рождения находится в интервале текущей даты до текущей даты + 7 дней
    #     if today.month <= bday_month <= end_date.month:
    #         if (today.month < bday_month or today.day <= bday_day) and (
    #                 bday_month < end_date.month or bday_day <= end_date.day):
    #             contacts_with_birthdays.append(contact)
    #
    # return contacts_with_birthdays

async def update_contact_status(body: ContactStatusUpdate, contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id)).first()

    if contact:
        contact.done = body.done
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id)).first()

    if contact:
        db.delete(contact)
        db.commit()
    return contact
