from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Errors.StaleFileNotFoundError import StaleFileNotFoundError
from todotree.Managers.StaleManager import StaleManager


class StaleAdd(AbstractCommand):

    def run(self, task_number):
        stale_manager = StaleManager(self.config)
        try:
            stale_manager.import_tasks()
        except StaleFileNotFoundError as e:
            e.echo_and_exit(self.config)
        except NoSuchTaskError as e:
            self.config.console.error(e.message)
            exit(1)
        self.taskManager.import_tasks()
        try:
            task_to_add = self.taskManager.remove_task_from_file(task_number)
        except NoSuchTaskError as e:
            self.config.console.error(e.message)
            exit(1)
        stale_manager.add_tasks_to_file([task_to_add])
        self.config.console.info("Added the following tasks to the stale list.")
        self.config.console.info(str(task_to_add))
        self.config.git.commit_and_push("Stale Add")
