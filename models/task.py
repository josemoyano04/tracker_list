from datetime import datetime
from models.status_task import status_task
from services.id_manager import IDManager 

class Task:
    
    def __init__(self, description: str, status: status_task):
        self.id = IDManager().assign_id()
        self.description = description
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def set_update_at(self):
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")