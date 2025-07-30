from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

class PortfolioItem(BaseModel):
    id: Optional[int] = None  # ✅ Default to None, so it's optional
    ticker: str = Field(..., example="AAPL")
    quantity: int = Field(..., gt=0)
    asset_type: str = Field(..., example="equity")
    purchase_price: float = Field(..., gt=0)
    purchase_date: date

    @validator("asset_type")
    def validate_asset_type(cls, v):
        allowed = ["equity", "bond", "cash"]
        if v.lower() not in allowed:
            raise ValueError("Asset type must be 'equity', 'bond', or 'cash'")
        return v.lower()

















