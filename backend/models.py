from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class PortfolioItem(BaseModel):
    id: Optional[int] = None  # ✅ Default to None, so it's optional
    ticker: str = Field(..., example="AAPL")
    quantity: int 
    asset_type: str = Field(..., example="equity")
    purchase_price: float = Field(..., gt=0)
    purchase_date: date
    balance:float

    @validator("asset_type")
    def validate_asset_type(cls, v):
        allowed = ["equity", "bond", "cash", "etf"]
        if v.lower() not in allowed:
            raise ValueError("Asset type must be 'equity', 'bond', 'cash', or 'etf'")
        return v.lower()
















