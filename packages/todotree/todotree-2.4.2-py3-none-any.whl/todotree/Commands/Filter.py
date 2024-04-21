import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError


class Filter(AbstractCommand):

    def run(self, search_term=None):
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)

        self.config.console.info(f"Todos for term '{search_term}'")
        self.taskManager.__str__(search_term)
        click.echo(self.taskManager)
