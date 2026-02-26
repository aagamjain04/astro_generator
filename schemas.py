from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class BirthDataRequest(BaseModel):
    full_name: str = Field(..., example="John Doe")
    date_of_birth: str = Field(..., example="1990-05-15") # YYYY-MM-DD
    time_of_birth: str = Field(..., example="14:30")       # HH:MM (24-hour)
    city: str = Field(..., example="New York")
    country: str = Field(..., example="USA")
    email: EmailStr
    gender: Optional[str] = Field("Not Specified", example="Male")