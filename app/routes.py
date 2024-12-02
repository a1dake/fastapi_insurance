from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import RatesSchema, InsuranceResponse
from .crud import get_rate, create_rate
from .utils import parse_rates_from_json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rates/")
def upload_rates(rates_data: RatesSchema, db: Session = Depends(get_db)):
    rates = parse_rates_from_json(rates_data.__root__)
    for rate in rates:
        create_rate(db, rate)
    return {"message": "Rates uploaded successfully"}

@router.post("/rates/file/")
async def upload_rates(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        import json
        rates_data = json.loads(contents)
        rates = parse_rates_from_json(rates_data)
        for rate in rates:
            create_rate(db, rate)
        
        return {"message": "Rates uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/insurance/", response_model=InsuranceResponse)
def calculate_insurance(
    cargo_type: str = Query(..., description="Тип груза"),
    declared_value: float = Query(..., description="Объявленная стоимость"),
    date: str = Query(..., description="Дата (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    rate = get_rate(db, cargo_type, date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    insurance_cost = declared_value * rate.rate
    return InsuranceResponse(insurance_cost=insurance_cost)
