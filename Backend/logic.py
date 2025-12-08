from pymongo import MongoClient
import datetime
import os  # <--- We added this library

class QueueSystem:
    def __init__(self):
        # <--- PASTE YOUR COPIED CLOUD STRING HERE --->
        # IMPORTANT: Replace YOUR_REAL_PASSWORD with the actual password you created
        cloud_url = "mongodb+srv://vikashkumar9504168773:Queue1234@cluster1.brit6sy.mongodb.net/?appName=Cluster1"
        
        # This tells the system: "Use the Cloud URL"
        mongo_url = os.getenv("MONGO_URL", cloud_url)
        
        self.client = MongoClient(mongo_url)
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
    
    def skip_next(self):
        """Marks the next waiting person as skipped (absent)"""
        # Find one person where status is 'waiting'
        next_person = self.collection.find_one_and_update(
            {"status": "waiting"},
            {"$set": {"status": "skipped"}}, # <--- Change status to skipped
            sort=[("joined_at", 1)],
            return_document=True
        )

        if next_person:
            next_person["id"] = str(next_person["_id"])
            del next_person["_id"]
            return next_person
        else:
            return None
        
    def get_skipped(self):
        """Get a list of all people who were skipped"""
        cursor = self.collection.find({"status": "skipped"})
        skipped_list = []
        for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            skipped_list.append(doc)
        return skipped_list

    def recall_customer(self, ticket_id):
        """Move a specific skipped person to 'serving'"""
        from bson.objectid import ObjectId # Need this to find by ID
        
        # 1. Update the specific person to 'serving'
        person = self.collection.find_one_and_update(
            {"_id": ObjectId(ticket_id)},
            {"$set": {"status": "serving"}},
            return_document=True
        )
        
        if person:
            person["id"] = str(person["_id"])
            del person["_id"]
            return person
        return None

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