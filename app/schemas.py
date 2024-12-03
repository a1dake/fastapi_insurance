from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date

class RateCreate(BaseModel):
    effective_date: date
    cargo_type: str
    rate: float

class InsuranceResponse(BaseModel):
    insurance_cost: float

class RateItem(BaseModel):
    cargo_type: str = Field(..., description="Тип груза")
    rate: float = Field(..., gt=0, description="Тариф")

class RatesSchema(BaseModel):
    __root__: Dict[str, List[RateItem]]

class RateUpdate(BaseModel):
    effective_date: date
    cargo_type: str
    rate: float

class RateDelete(BaseModel):
    effective_date: date
    cargo_type: str

class RateOut(BaseModel):
    id: int
    effective_date: date
    cargo_type: str
    rate: float

    class Config:
        orm_mode = True