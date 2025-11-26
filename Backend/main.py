from fastapi import FastAPI
from pydantic import BaseModel
from logic import QueueSystem

app = FastAPI()
queue_system = QueueSystem()

class CustomerInput(BaseModel):
    name: str

@app.get("/")
def home():
    return {"message": "Queue System Online"}  # <--- Note the new message!

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
        "waiting": len(queue_system.queue),
        "serving": queue_system.currently_serving
    }