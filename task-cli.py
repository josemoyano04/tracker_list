import click
from models.task import Task, StatusTask
from storage.storage_manager import StorageManager
from services.id_manager import IDManager

@click.group
def cli():
    pass

IDManager.validate_id_counter() #Valida la consistencia de inicio de contador.(Si el storage no existe, countador = 1)
storage = StorageManager()

@cli.command()
@click.argument("description")
def add(description):
    task = Task( 
        description= description,
    )
    
    storage.add_task(task)
    click.echo(f"Task added successfully (ID: {task.id})")

@cli.command() #TODO imlementar option para usar list para obtener todas las tareas, o filtradas por status.
@click.argument("status", 
               type= click.Choice([status.value.lower() for status in StatusTask]))    
def list(status: str):
    tasks = storage.get_tasks_for_status(status.upper())
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


if __name__ == "__main__":
    cli()