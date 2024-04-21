from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFoundError import DoneFileNotFoundError
from todotree.Managers.DoneManager import DoneManager


class ListDone(AbstractCommand):
    def run(self):
        try:
            done_manager = DoneManager(self.config)
            done_manager.import_tasks()
            self.config.console.info(done_manager)
        except DoneFileNotFoundError as e:
            e.echo_and_exit(self.config)
