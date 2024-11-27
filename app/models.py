from sqlalchemy.orm import Session
from .database import Number

def create_number(db: Session, value: int):
    db_number = Number(value=value)
    db.add(db_number)
    db.commit()
    db.refresh(db_number)
    return db_number

def get_number(db: Session, value: int):
    return db.query(Number).filter(Number.value == value).first()

def get_max_number(db: Session):
    return db.query(Number).order_by(Number.value.desc()).first()