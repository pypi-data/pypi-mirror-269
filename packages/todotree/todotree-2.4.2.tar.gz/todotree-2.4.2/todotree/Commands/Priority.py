from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError
from todotree.Task.Task import Task


class Priority(AbstractCommand):
    def run(self, task_number: int, new_priority: str):
        # Disable fancy imports.
        self.config.enable_project_folder = False
        # Run task.
        try:
            self.taskManager.import_tasks()
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        new_task = self.taskManager.add_or_update_task(task_number, Task.add_or_update_priority,
                                                       new_priority.upper())
        self.config.console.info("The new task is: ")
        self.config.console.info(new_task)
        self.config.git.commit_and_push("priority")
