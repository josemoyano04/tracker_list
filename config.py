import os

#Storage manager
STORAGE_NAME = "storage_task.json"
STORAGE_PATH = os.path.join(os.path.dirname(__name__), "storage", STORAGE_NAME)

#Id manager
ID_COUNTER_NAME = "id_counter.json"
ID_COUNTER_PATH = os.path.join(os.path.dirname(__name__), "services", ID_COUNTER_NAME)