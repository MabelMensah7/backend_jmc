from fastapi import APIRouter, HTTPException
from datetime import date, datetime
from bson.objectid import ObjectId

from app.models import Appointment
from app.database import appointments_collection
from app.email_utils import send_email, ADMIN_EMAIL

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("")
def book_appointment(appointment: Appointment):
    # Disallow past dates
    if appointment.date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Appointment date must be in the future."
        )

    # Convert unsupported datetime.date and datetime.time to strings for MongoDB
    appointment_dict = appointment.model_dump()
    appointment_dict["date"] = appointment.date.isoformat()
    appointment_dict["time"] = appointment.time.isoformat()

    # Insert appointment
    try:
        result = appointments_collection.insert_one(appointment_dict)

        # Format date and time nicely for email
        dt = datetime.combine(appointment.date, appointment.time)
        formatted_dt = dt.strftime("%A, %B %d, %Y at %I:%M %p")

        # EMAIL TO CLIENT
        client_body = f"""
Appointment Confirmation

Dear {appointment.full_name},

Thank you for booking with Japan Medical Center!

Appointment Details:
Date: {formatted_dt}
Department: {appointment.department}
Phone: {appointment.phone}
Notes: {appointment.notes}

We’ll contact you soon to confirm your appointment.

Warm regards,
Japan Medical Center Team
"""
        send_email(
            subject="Your Appointment is Confirmed",
            recipient=appointment.email,
            body=client_body
        )

        # EMAIL TO HOSPITAL ADMIN
        admin_body = f"""
New Appointment Received:

Full Name: {appointment.full_name}
Email: {appointment.email}
Phone: {appointment.phone}
Department: {appointment.department}
Appointment Date: {formatted_dt}
Notes: {appointment.notes}
"""
        send_email(
            subject="New Appointment Received",
            recipient=ADMIN_EMAIL,
            body=admin_body
        )

        return {"id": str(result.inserted_id), "message": "Appointment booked successfully"}

    except Exception as e:
        if "duplicate key error" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail="This time slot is already booked. Please choose another."
            )
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_appointments():
    appointments = list(appointments_collection.find())
    for a in appointments:
        a["_id"] = str(a["_id"])
    return appointments


@router.get("/{appointment_id}")
def get_appointment(appointment_id: str):
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment["_id"] = str(appointment["_id"])
    return appointment
