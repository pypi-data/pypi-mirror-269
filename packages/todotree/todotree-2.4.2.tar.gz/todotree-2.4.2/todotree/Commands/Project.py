import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError


class Project(AbstractCommand):

    def run(self):
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        # Print due tree.
        click.echo(self.taskManager.print_tree("projects"))
