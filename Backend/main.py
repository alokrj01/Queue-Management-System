from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- NEW IMPORT
from pydantic import BaseModel
from logic import QueueSystem

app = FastAPI()

# <--- NEW: ALLOW REACT TO TALK TO PYTHON --->
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_system = QueueSystem()

class CustomerInput(BaseModel):
    name: str

@app.get("/")
def home():
    return {"message": "Queue System Online"}

@app.post("/join")
def join_queue(data: CustomerInput):
    return queue_system.add_customer(data.name)

@app.post("/next")
def call_next():
    person = queue_system.call_next()
    if person is None:
        return {"message": "No one is waiting!"}
    return {"message": "Now serving", "person": person}

@app.get("/status")
def check_status():
    return {
        "waiting_count": queue_system.get_queue_length(),
        "message": "System Active"
    }