from pydantic import BaseModel, EmailStr, Field
from datetime import date, time

class Appointment(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    department: str
    date: date
    time: time
    notes: str | None = None

class ContactMessage(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    message: str
