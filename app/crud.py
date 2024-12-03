from sqlalchemy.orm import Session
from app.models import Rate
from app.schemas import RateCreate
from datetime import date

def get_rate(db: Session, cargo_type: str, date: str):
    return (
        db.query(Rate)
        .filter(Rate.cargo_type == cargo_type, Rate.effective_date == date)
        .order_by(Rate.effective_date.desc())
        .first()
    )

def create_rate(db: Session, rate: RateCreate):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def update_rate(db: Session, effective_date: date, cargo_type: str, rate_value: float):
    rate = db.query(Rate).filter(
        Rate.effective_date == effective_date,
        Rate.cargo_type == cargo_type
    ).first()

    if not rate:
        return None

    rate.rate = rate_value
    db.commit()
    db.refresh(rate)
    return rate


def delete_rate(db: Session, effective_date: date, cargo_type: str):
    rate = db.query(Rate).filter(
        Rate.effective_date == effective_date,
        Rate.cargo_type == cargo_type
    ).first()

    if rate:
        db.delete(rate)
        db.commit()
        return True
    return False