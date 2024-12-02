from sqlalchemy.orm import Session
from .models import Rate
from .schemas import RateCreate

def get_rate(db: Session, cargo_type: str, date: str):
    return (
        db.query(Rate)
        .filter(Rate.cargo_type == cargo_type, Rate.effective_date <= date)
        .order_by(Rate.effective_date.desc())
        .first()
    )

def create_rate(db: Session, rate: RateCreate):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate
