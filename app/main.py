from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.appointments import router as appointments_router
from app.routes.contacts import router as contacts_router

# 1. Create the FastAPI app
app = FastAPI(title="Japan Medical Center API", version="1.0")

# 2. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins; in production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include your routers
app.include_router(appointments_router)
app.include_router(contacts_router)

# 4. Root endpoint
@app.get("/")
def root():
    return {"message": "Japan Medical Center API is running"}
# why does it say i have no main