import os
import json
import config as c
from typing import List
from models.task import Task
from errors.task_not_exists_error import TaskNotExistsError

class StorageManager:
    #Singleton class
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(cls, StorageManager).__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, "__initialized"):
            self.__initialized = True 
            self._storage_exists = os.path.exists(c.STORAGE_PATH)
            if not self._storage_exists:
                self._create_storage() #Creacion de almacenamiento y seteo de _storage_exists

    
    #Methods
    def add_task(self, task: Task): 
        #Validaciones
        if not self._storage_exists: #Validacion de almacenamiento existente.
            raise FileNotFoundError("Error, storage file does not exist.")
        if not isinstance(task, Task): #Validación de tipo.
            raise TypeError("Error trying to add object, apparently it is not a 'Task' instance")
        
        
        #Lectura de json.
        with open(c.STORAGE_PATH, "r") as storage:
            st = json.load(storage)
            st[str(task.id)] = task.to_dict()
        
        #Guardado de json.   
        with open(c.STORAGE_PATH, "w") as storage:
            json.dump(st, storage, indent= 4)
      
    def get_task_for_id(self, task_id: int) -> Task: 
        #Validaciones
        if not self._storage_exists: #Validacion de almacenamiento existente.
            raise FileNotFoundError("Error, storage file does not exist.")
        
        self._validate_id(task_id) #Validacion de id.
        
        if not self._task_exists(task_id): #Validacion de existencia de tarea.
            raise TaskNotExistsError("Id does not correspond to an existing task.")
        
        #Lectura y obtencion de tarea:
        with open(c.STORAGE_PATH, "r") as storage:
            st = json.load(storage)
            task = st[str(task_id)]
            return Task.dict_to_task(task)
      
    def get_tasks_for_status(self, status: str) -> List[Task]: 
        #Validaciones
        if not self._storage_exists: #Validacion de almacenamiento existente.
            raise FileNotFoundError("Error, storage file does not exist.")
      
        #Lectura y obtencion de tarea:
        with open(c.STORAGE_PATH, "r") as storage:
            st: dict = json.load(storage)
            tasks = []
            for task in st.values():
                if task["status"] == status:
                    tasks.append(Task.dict_to_task(task))
                    
            return tasks #Devolucion de tareas filtradas.
    
    def get_all_task(self) -> List[Task]:
        #Validaciones:
        if not self._storage_exists:
            raise FileNotFoundError("Error, storage file does not exist.")
        
        #Lectura y obtención de datos:
        with open(c.STORAGE_PATH, "r") as storage:
            st = json.load(storage)    
            return [Task.dict_to_task(task) for task in st.values()]
          
    def update_task(self, task_id: int, updated_task: Task):
        #Validaciones
        if not self._storage_exists: #Validacion de almacenamiento existente.
            raise FileNotFoundError("Error, storage file does not exist.")
        
        self._validate_id(task_id) #Validacion de id.
        
        if not isinstance(updated_task, Task): #Validacion de tipo.
            raise TypeError("Error trying to update task, apparently 'update_task' it is not a 'Task' instance")
        
        if not self._task_exists(task_id): #Validacion de existencia de tarea.
            raise TaskNotExistsError("Id does not correspond to an existing task.")
        
        
        #Lectura y modificación de json:
        with open(c.STORAGE_PATH, "r") as storage:
            #Lectura
            st = json.load(storage)
            #Modificacion
            updated_task.id = task_id #Reasignacion de id
            updated_task.set_update_at() #Actualizacion de fecha de ultimo update.
            st[str(task_id)] = updated_task.to_dict() #Sobreescritura de tarea en json.
        
        #Guardado de json
        with open(c.STORAGE_PATH, "w") as storage:
            json.dump(st, storage, indent= 4)
    
    def delete_task(self, task_id: int):
        #Validaciones
        if not self._storage_exists: #Validacion de almacenamiento existente.
            raise FileNotFoundError("Error, storage file does not exist.")
        
        self._validate_id(task_id) #Validacion de id.
        
        if not self._task_exists(task_id): #Validación de existencia de tarea.
            raise TaskNotExistsError("Id does not correspond to an existing task.")
        
        
        #Lectura y eliminación:
        with open(c.STORAGE_PATH, "r") as storage:
            st = json.load(storage)
            del st[str(task_id)]
        
        #Guardado de cambios:
        with open(c.STORAGE_PATH, "w") as storage:
            json.dump(st, storage, indent= 4)

    #Aux methods
    def _task_exists(self, task_id: int) -> bool:
        self._validate_id(task_id) #Lanza TypeError si no es entero o ValueError si es negativo.
        
        #Lectura de json:
        with open(c.STORAGE_PATH, "r") as storage:
            st = json.load(storage)
            return str(task_id) in st
    
    def _create_storage(self) ->  None:
        if not os.path.exists(c.STORAGE_PATH):
            with open(c.STORAGE_PATH, "w") as storage:
                json.dump({}, storage)
                self._storage_exists = True
        
    def _validate_id(self, id: int) -> None:
        try:
            id = int(id)  # Intentar convertir a entero
        except ValueError:
            raise TypeError("ID is not integer.")
            
        if id <= 0: #Validacion de numero positivo.
            raise ValueError("ID cannot be negative or zero.")