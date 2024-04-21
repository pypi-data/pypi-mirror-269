import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError


class Context(AbstractCommand):

    def run(self):
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        click.echo(self.taskManager.print_tree("contexts"))
