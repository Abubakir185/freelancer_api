from sqlalchemy.orm import Session
import models, schema

def get_users(db: Session):
    return db.query(models.Freelancer).all()

def get_user(db: Session, user_id: int):
    return db.query(models.Freelancer).filter(models.Freelancer.id == user_id).first()

def create_user(db: Session, user: schema.FreelancerCreate):
    db_user = models.Freelancer(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: schema.FreelancerUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for field, value in user_data.dict().items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_users_by_skill(db: Session, skill: str):
    users = db.query(models.Freelancer).all()
    return [user for user in users if skill in user.skills]
