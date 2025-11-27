from pymongo import MongoClient
import datetime
import os  # <--- We added this library

class QueueSystem:
    def __init__(self):
        # <--- THIS IS THE NEW PART --->
        # It looks for a "MONGO_URL" environment variable. 
        # If it doesn't find one (like on your laptop), it uses "localhost".
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        
        self.client = MongoClient(mongo_url)
        # <--- END OF NEW PART --->

        self.db = self.client["queue_db"]
        self.collection = self.db["tickets"]

    def add_customer(self, name):
        ticket = {
            "name": name,
            "status": "waiting",
            "joined_at": datetime.datetime.now()
        }
        result = self.collection.insert_one(ticket)
        ticket["id"] = str(result.inserted_id)
        del ticket["_id"]
        return ticket

    def call_next(self):
        next_person = self.collection.find_one_and_update(
            {"status": "waiting"},
            {"$set": {"status": "serving"}},
            sort=[("joined_at", 1)],
            return_document=True
        )

        if next_person:
            next_person["id"] = str(next_person["_id"])
            del next_person["_id"]
            return next_person
        else:
            return None

    def get_queue_length(self):
        return self.collection.count_documents({"status": "waiting"})