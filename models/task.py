from datetime import datetime
from models.status_task import StatusTask
from services.id_manager import IDManager 

class Task:
    
    def __init__(self, description: str, 
                 status: str = None, 
                 id: int= None, 
                 create_at: str = None,
                 updated_at: str = None):
        self.id: int = IDManager().assign_id() if id is None else id
        self.description: str = description
        self.status: str = StatusTask.todo.value if status is None else status
        self.created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M") if create_at is None else create_at
        self.updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M") if updated_at is None else updated_at
        
    #Methods
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
    
    #Class methods
    @classmethod
    def dict_to_task(cls, json_task: dict):
        return Task(id= int(json_task["id"]),
                    description= json_task["description"],
                    status= json_task["status"],
                    create_at= json_task["created_at"],
                    updated_at= json_task["updated_at"])
        
    #Reassigned methods
    def __str__(self):
        string = f"""id: {self.id}
description: {self.description}
status: {self.status}
created at: {self.created_at}
updated at: {self.updated_at}
*****************************"""
        return string