from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logic import QueueSystem
import joblib # <--- NEW IMPORT
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_system = QueueSystem()

# <--- LOAD THE AI MODEL --->
# We check if the file exists first to avoid errors
if os.path.exists("wait_time_model.pkl"):
    ai_model = joblib.load("wait_time_model.pkl")
else:
    ai_model = None

class CustomerInput(BaseModel):
    name: str

@app.get("/")
def home():
    return {"message": "Queue System Online"}

@app.post("/join")
def join_queue(data: CustomerInput):
    ticket = queue_system.add_customer(data.name)
    
    # <--- CALCULATE AI PREDICTION --->
    prediction = 0
    if ai_model:
        # Count people waiting (minus the one we just added)
        count = queue_system.get_queue_length() - 1
        if count < 0: count = 0
        
        # Ask the AI
        prediction = ai_model.predict([[count]])[0]
        prediction = round(prediction)
    
    # <--- THE FIX: Add the time DIRECTLY to the ticket --->
    ticket["estimated_wait_minutes"] = prediction
    
    # Return the simple ticket (Frontend will be happy now)
    return ticket

@app.post("/next")
def call_next():
    person = queue_system.call_next()
    if person is None:
        return {"message": "No one is waiting!"}
    return {"message": "Now serving", "person": person}

@app.post("/skip")
def skip_customer():
    person = queue_system.skip_next()
    if person is None:
        return {"message": "No one is waiting to skip!"}
    return {"message": "Skipped customer", "person": person}
@app.get("/skipped")
def get_skipped_list():
    return queue_system.get_skipped()

@app.post("/recall/{ticket_id}")
def recall_customer(ticket_id: str):
    person = queue_system.recall_customer(ticket_id)
    if person is None:
        return {"message": "Customer not found"}
    return {"message": "Recalling customer", "person": person}

@app.get("/status")
def check_status():
    return {
        "waiting_count": queue_system.get_queue_length(),
        "message": "System Active"
    }