import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFoundError import DoneFileNotFoundError
from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError
from todotree.Managers.DoneManager import DoneManager
from todotree.Task.Task import Task


class Revive(AbstractCommand):
    def run(self, done_number: int):
        done_manager = DoneManager(self.config)
        try:
            done_manager.import_tasks()
            revived_task = done_manager.remove_task_from_file(done_number)
        except DoneFileNotFoundError as e:
            e.echo_and_exit(self.config)
            exit(1)  # Never reached.
        except NoSuchTaskError as e:
            self.config.console.error(e.message)
            exit(1)
        try:
            self.taskManager.import_tasks()
            new_tasks = self.taskManager.add_tasks_to_file([Task(revived_task.i, revived_task.task_string)])
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        self.config.console.info("The newly revived tasks:")
        for task in new_tasks:
            self.config.console.info(str(task))
        self.config.git.commit_and_push("revive")
