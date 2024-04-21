import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError


class Due(AbstractCommand):
    def run(self):
        # Disable fancy imports, because they do not have due dates.
        self.config.enable_project_folder = False
        # Import tasks.
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        # Print due tree.
        click.echo(self.taskManager.print_tree("due"))
