from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    effective_date = Column(Date, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float, nullable=False)
