# database.py
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
import os

# MongoDB connection URI (ensure your credentials are correct)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://jmc_backend:jmc_backend@grow-cohort6.fwryawq.mongodb.net/"
)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["jmc_backend"]

# Collections
contacts_collection = db["contacts"]
appointments_collection = db["appointments"]

# Safe index creation for appointments
try:
    appointments_collection.create_index(
        [("department", ASCENDING), ("date", ASCENDING), ("time", ASCENDING)],
        unique=True,
        background=True  # creates the index in background so it won't block operations
    )
    print("Appointments index created successfully.")
except DuplicateKeyError:
    print("Warning: Duplicate entries exist. Unique index was not fully created.")
except Exception as e:
    print(f"Error creating index: {e}")

