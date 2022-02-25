from sqlalchemy.orm import Session
import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.user).filter(models.user.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.user).filter(models.user.DedeUserID == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.user).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.Createuser):
    db_user = models.user(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

