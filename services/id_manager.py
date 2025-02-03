import os
import json
import config as c

class IDManager():
    #Singleton class
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(cls, IDManager).__new__(cls)
        return cls.__instance
    def __init__(self):
        if not hasattr(self, "__initialized"):
            self.__initialized = True
            self.__exist_counter = os.path.exists(c.ID_COUNTER_PATH)
            if not self.__exist_counter:
                self._create_id_counter()

    #Methods
    def assign_id(self) -> int:
        #Escritura y obtención de id
        with open(c.ID_COUNTER_PATH, "r") as id_counter:
            counter = json.load(id_counter)
            id_to_assign = counter["counter"]
            counter["counter"] = id_to_assign + 1
        
        #Guardado de cambios:
        with open(c.ID_COUNTER_PATH, "w") as id_counter:
            json.dump(counter, id_counter, indent= 4)
            
        return id_to_assign
    
    def _create_id_counter(self) -> None:
        with open(c.ID_COUNTER_PATH, "w") as id_counter:
            json.dump({"counter": 1}, id_counter, indent=4)