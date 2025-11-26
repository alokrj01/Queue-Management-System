from collections import deque

class QueueSystem:
    def __init__(self):
        self.queue = deque()
        self.current_ticket_num = 0
        self.currently_serving = None

    def add_customer(self, name):
        self.current_ticket_num += 1
        ticket = {
            "id": self.current_ticket_num,
            "name": name,
            "status": "waiting"
        }
        self.queue.append(ticket)
        return ticket

    def call_next(self):
        if len(self.queue) == 0:
            return None
        next_person = self.queue.popleft()
        next_person["status"] = "serving"
        self.currently_serving = next_person
        return next_person