from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.model import Contact
from src.schemas import ContactModel, ContactStatusUpdate


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(name=body.name,surname=body.surname, email=body.email,mobile=body.mobile)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(skip: int, limit: int, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id)).offset(skip).limit(limit).all()
    return contact


async def get_contact(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def update_contact(body: ContactModel, contact_id: int, db: Session):
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
                              email: str | None, db: Session):
    contacts = db.query(Contact)

    if name:
        contacts = contacts.filter(Contact.name.like(f"%{name}%"))
    if surname:
        contacts = contacts.filter(Contact.surname.like(f"%{surname}%"))
    if email:
        contacts = contacts.filter(Contact.email.like(f"%{email}%"))
    print(f"name: {name}, surname: {surname}, email: {email}")

    contact = contacts.first()
    return contact


async def get_contacts_birthdays(db: Session):
    seven_days_from_now = datetime.now().date() + timedelta(days=7)
    contacts = db.query(Contact).all()

    contacts_with_birthdays = [
        contact for contact in contacts if
        datetime.now().date().day <= contact.date_of_birth.day < seven_days_from_now.day
    ]
    print(f"{contacts_with_birthdays=}")

    return contacts_with_birthdays


async def update_contact_status(body: ContactStatusUpdate, contact_id: int, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id)).first()

    if contact:
        contact.done = body.done
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id==contact_id, Contact.user_id == user.id)).first()

    if contact:
        db.delete(contact)
        db.commit()
    return contact
