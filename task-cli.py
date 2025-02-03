import click
from models.task import Task, status_task
from storage.storage_manager import StorageManager

@click.group
def cli():
    pass

storage = StorageManager()

@cli.command()
@click.argument("description")
@click.option ("--status", "-s", 
               default= status_task.todo.value, 
               type= click.Choice([status.value for status in status_task]))

def add(description, status):
    task = Task( 
        description= description,
        status= status
    )
    
    storage.add_task(task)
    click.echo(f"Task added successfully (ID: {task.id})")
    
if __name__ == "__main__":
    cli()