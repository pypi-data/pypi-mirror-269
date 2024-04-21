from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Errors.StaleFileNotFoundError import StaleFileNotFoundError
from todotree.Managers.StaleManager import StaleManager


class StaleRevive(AbstractCommand):

    def run(self, task_number):
        stale_manager = StaleManager(self.config)
        try:
            stale_manager.import_tasks()
        except StaleFileNotFoundError as e:
            e.echo_and_exit(self.config)
        try:
            revived_task = stale_manager.remove_task_from_file(task_number)
        except NoSuchTaskError as e:
            self.config.console.error(e.message)
            exit(1)
        self.taskManager.import_tasks()
        self.taskManager.add_tasks_to_file([revived_task])

        self.config.console.info("Revived the following task:")
        self.config.console.info(str(revived_task))
        self.config.git.commit_and_push("Stale Revive")
