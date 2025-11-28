from pymongo import MongoClient
import random
import datetime

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["queue_db"]
collection = db["tickets"]

print("🌱 Seeding Database with 500 past customers...")

fake_data = []

for i in range(500):
    # Randomly decide how many people were waiting (0 to 15)
    people_ahead = random.randint(0, 15)
    
    # Calculate how long they waited (approx 4 mins per person + random noise)
    wait_minutes = (people_ahead * 4) + random.randint(-3, 5)
    if wait_minutes < 1: wait_minutes = 1
    
    # Create a fake "Completed" ticket
    ticket = {
        "name": f"Customer-{i}",
        "status": "completed",  # These people are already served
        "people_ahead_when_joined": people_ahead, # The INPUT for AI
        "actual_wait_minutes": wait_minutes,      # The OUTPUT for AI
        "joined_at": datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    }
    fake_data.append(ticket)

# Insert all at once
collection.insert_many(fake_data)
print("✅ Success! Added 500 records to MongoDB.")