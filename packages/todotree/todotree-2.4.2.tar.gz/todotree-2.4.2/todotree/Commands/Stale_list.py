from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.StaleFileNotFoundError import StaleFileNotFoundError
from todotree.Managers.StaleManager import StaleManager


class StaleList(AbstractCommand):

    def run(self):
        stale_manager = StaleManager(self.config)
        try:
            stale_manager.import_tasks()
        except StaleFileNotFoundError as e:
            e.echo_and_exit(self.config)
        self.config.console.info(stale_manager.__str__())
