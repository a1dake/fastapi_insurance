from typing import Dict, List
from datetime import datetime
from .schemas import RateCreate, RateItem

def parse_rates_from_json(json_data: Dict[str, List[RateItem]]):
    rates = []
    for date, entries in json_data.items():
        effective_date = datetime.strptime(date, "%Y-%m-%d").date()
        for entry in entries:
            rates.append(RateCreate(
                effective_date=effective_date,
                cargo_type=entry.cargo_type,
                rate=entry.rate
            ))
    return rates
