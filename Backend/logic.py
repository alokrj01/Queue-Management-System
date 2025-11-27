from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

class QueueSystem:
    def __init__(self):
        # 1. Connect to MongoDB (Default Localhost settings)
        # If using Cloud/Atlas, replace the URL below with your connection string
        self.client = MongoClient("mongodb://localhost:27017/")
        
        # 2. Select the Database and Collection
        self.db = self.client["queue_db"]
        self.collection = self.db["tickets"]

    def add_customer(self, name):
        """Adds a person to the MongoDB database"""
        ticket = {
            "name": name,
            "status": "waiting",
            "joined_at": datetime.datetime.now()
        }
        # Insert into DB
        result = self.collection.insert_one(ticket)
        
        # Convert the Database ID to a string so we can read it
        ticket["id"] = str(result.inserted_id)
        # Remove the internal ID object to avoid errors sending to frontend
        del ticket["_id"] 
        return ticket

    def call_next(self):
        """Finds the oldest waiting person and updates them to 'serving'"""
        # Find one person where status is 'waiting', sort by oldest time
        next_person = self.collection.find_one_and_update(
            {"status": "waiting"},
            {"$set": {"status": "serving"}},
            sort=[("joined_at", 1)], # 1 means Oldest first (FIFO)
            return_document=True
        )

        if next_person:
            next_person["id"] = str(next_person["_id"])
            del next_person["_id"]
            return next_person
        else:
            return None

    def get_queue_length(self):
        """Count how many people are waiting"""
        return self.collection.count_documents({"status": "waiting"})