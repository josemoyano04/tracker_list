
class TaskNotExistsError(Exception):
    #Excepcion definida por usuario para tareas no existentes
    def __init__(self, *args):
        super().__init__(*args)