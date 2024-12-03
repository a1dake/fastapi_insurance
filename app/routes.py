from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
# from app.producer import log_action
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import RatesSchema, InsuranceResponse, RateDelete, RateUpdate, RateOut
from app.crud import get_rate, create_rate, update_rate, delete_rate
from app.utils import parse_rates_from_json

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

@router.put("/rates", response_model=RateOut)
def edit_rate(rate_data: RateUpdate, db: Session = Depends(get_db)):
    updated_rate = update_rate(
        db=db,
        effective_date=rate_data.effective_date,
        cargo_type=rate_data.cargo_type,
        rate_value=rate_data.rate
    )
    if not updated_rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    # log_action(
    #     action=f"Edited rate with Date {rate_data.effective_date}, Cargo type {rate_data.cargo_type}. Cahange: rate {rate_data.rate}",
    #     timestamp=datetime.utcnow(),
    # )
    return updated_rate

@router.delete("/rates")
def remove_rate(rate_data: RateDelete, db: Session = Depends(get_db)):
    success = delete_rate(
        db=db,
        effective_date=rate_data.effective_date,
        cargo_type=rate_data.cargo_type
    )
    if not success:
        raise HTTPException(status_code=404, detail="Rate not found")
    # log_action(
    #     action=f"Deleted rate with Date {rate_data.effective_date}, Cargo type {rate_data.cargo_type}",
    #     timestamp=datetime.utcnow(),
    # )
    return {"message": "Rate deleted successfully"}

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


