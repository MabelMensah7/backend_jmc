from fastapi import APIRouter
from bson.objectid import ObjectId

from app.models import ContactMessage
from app.database import contacts_collection
from app.email_utils import send_email, ADMIN_EMAIL

router = APIRouter(prefix="/contact", tags=["Contact Forms"])

@router.post("")
def send_contact_message(message: ContactMessage):
    result = contacts_collection.insert_one(message.dict())

    # Notify admin
    admin_body = f"""
New Contact Message:

Name: {message.full_name}
Email: {message.email}
Phone: {message.phone}

Message:
{message.message}
"""
    send_email(
        subject="New Contact Message",
        recipient=ADMIN_EMAIL,
        body=admin_body
    )

    return {"id": str(result.inserted_id), "message": "Message sent successfully"}
