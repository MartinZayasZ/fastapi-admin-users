from sqlalchemy.orm import Session
from sqlalchemy import update

from .config import schemas, models

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_and_password(db: Session, email: str, password: str):
    # La contraseña debe venir con security.encode_password
    return db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

def create_user(db: Session, user: schemas.UserIn, created_by: int | None = None):
    db_user = models.User(**user.dict(), created_by=created_by)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate, id: int = id, updated_by: int | None = None):
    user_to_update = dict((k, v) for k, v in user.dict().items() if v is not None)
    db.execute(update(models.User).where(models.User.id == id).values(**user_to_update, updated_by=updated_by))
    db.commit()