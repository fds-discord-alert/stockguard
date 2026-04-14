from pydantic import BaseModel

class Transaction(BaseModel):
    user_id: str
    amount: int
    timestamp: str  # "HH:MM" 형식
    location: str   # "Korea", "USA" 등
    stock_name: str