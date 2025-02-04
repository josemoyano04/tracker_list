import os
import click
import config
from models.task import Task, StatusTask
from storage.storage_manager import StorageManager
from services.id_manager import IDManager

@click.group
def cli():
    pass

IDManager.validate_id_counter() #Valida la consistencia de inicio de contador.(Si el storage no existe, countador = 1)
storage = StorageManager()

#CRUD methods
@cli.command()
@click.argument("description")
def add(description):
    task = Task( 
        description= description,
    )
    
    storage.add_task(task)
    click.echo(f"Task added successfully (ID: {task.id})")

@cli.command()
@click.argument("status", 
               type= click.Choice([status.value.lower() for status in StatusTask]),
               required= False)    
def list(status: str):
    tasks = storage.get_all_task() if not status else storage.get_tasks_for_status(status.upper())
    
    message_not_found_tasks = f"No task with status {status} was found." if status else "There is no task."
    
    #Validacion de tareas encontradas:
    if len(tasks) == 0:
        click.echo(message_not_found_tasks)
    
    else:
        for task in tasks:
            click.echo(task)
    
@cli.command()
@click.argument("id")
@click.argument("description")
def update(id: int, description: str):
    task = storage.get_task_for_id(id)
    updated_task = Task(id= id,
                        description= description,
                        status= task.status,
                        create_at= task.created_at,
                        updated_at= task.updated_at) 
    
    task_id = int(id)
    storage.update_task(task_id, updated_task)
    click.echo(f"Task updated successfully (ID: {id})")

@cli.command()
@click.argument("id")
def delete(id: int):
    storage.delete_task(id)    
    click.echo(f"Task delete successfully (ID: {id})")


#Status marking method
@cli.command()
@click.argument("id")
def mark_todo(id: int):
    task = storage.get_task_for_id(id)
    task.status = StatusTask.todo.value
    storage.update_task(id, task)

@cli.command()
@click.argument("id")
def mark_in_progress(id: int):
    task = storage.get_task_for_id(id)
    task.status = StatusTask.in_progress.value
    storage.update_task(id, task)

@cli.command()
@click.argument("id")
def mark_done(id: int):
    task = storage.get_task_for_id(id)
    task.status = StatusTask.done.value
    storage.update_task(id, task)

#Extra methods
@cli.command()
def reset_system():
    if click.confirm("Confirm delete storage and reboot system?"):
        os.remove(config.STORAGE_PATH)
        click.echo("System rebooted successfully.")

if __name__ == "__main__":
    cli()