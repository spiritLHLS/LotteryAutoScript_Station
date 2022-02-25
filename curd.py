from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.user).filter(models.user.id == user_id).first()


def get_user_by_name(db: Session, DedeUserID: str):
    return db.query(models.user).filter(models.user.DedeUserID == DedeUserID).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.user).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.Createuser):
    db_user = models.user(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_by_code(db: Session, user):
    db_user = models.user(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_user_by_code(db: Session, user):
    db_user = models.user(**user)
    mod_user = db.query(models.user).filter(models.user.DedeUserID == db_user.DedeUserID).first()
    mod_user.SESSDATA = db_user.SESSDATA
    mod_user.bili_jct = db_user.bili_jct
    mod_user.email = db_user.email
    db.commit()
    db.refresh(mod_user)
    return mod_user


def delete_user_by_code(db: Session, DedeUserID: str):
    mod_user = db.query(models.user).filter(models.user.DedeUserID == DedeUserID).first()
    db.delete(mod_user)
    db.commit()
    return mod_user