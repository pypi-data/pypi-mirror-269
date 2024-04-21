import math
import shutil
from abc import ABC
from pathlib import Path
# https://docs.python.org/3/library/tempfile.html
from tempfile import NamedTemporaryFile

from todotree.Errors.NoSuchTaskError import NoSuchTaskError
from todotree.Task.ConsoleTask import ConsoleTask
from todotree.Task.Task import Task


class AbstractManager(ABC):
    not_found_error = FileNotFoundError
    """Error to raise when the database file is not found."""

    @property
    def max_task_number(self) -> int:
        """Property which defines the highest number in the task list."""
        try:
            return max([x.i for x in self.task_list])
        except ValueError:
            # Then the list is empty
            return 0

    @property
    def number_of_digits(self) -> int:
        """Property which defines the number of digits of the task in the task list with the highest number."""
        maxi = max([x.i for x in self.task_list])
        return int(math.ceil(math.log(self.max_task_number + 1, 10)))

    def __init__(self):
        self.file: Path = Path("/")
        """Path to the 'database' file. Must be set in the subclass."""

        self.task_list: list[Task] = []
        """Task list"""

    def remove_task_from_file(self, task_number: int) -> Task:
        # Remove task.
        return self.remove_tasks_from_file([task_number])[0]

    def remove_tasks_from_file(self, task_numbers: list[int]) -> list[Task]:
        removed_tasks = [tasks for tasks in self.task_list if tasks.i in task_numbers]
        if len(removed_tasks) != len(task_numbers):
            # One or more are missing, diff the sets, convert to string.
            set_diff = set(task_numbers) - set([tasks.i for tasks in removed_tasks])
            missed_tasks = ', '.join([str(i) for i in set_diff])
            # Raise an error.
            raise NoSuchTaskError(f"Task{'s' if len(set_diff) != 1 else ''} {missed_tasks} does not exist in {self.file}.")
        # Remove tasks.
        self.task_list = [tasks for tasks in self.task_list if tasks.i not in task_numbers]
        self.write_to_file()
        return removed_tasks

    def write_to_file(self):
        """Writes the entire list to the file."""
        # Sort task list.
        self.task_list.sort(key=lambda x: x.i)
        #  Delete=false is needed for windows, I hope that somebodies temp folder won't be clobbered with this...
        try:
            with NamedTemporaryFile("w+t", newline="", delete=False) as temp_file:
                # may strip new lines by using task list.
                for task in self.task_list:
                    temp_file.write(task.to_file())
                temp_file.flush()
                shutil.copy(temp_file.name, self.file)
        except FileNotFoundError as e:
            raise self.not_found_error from e

    def add_tasks_to_file(self, tasks: list[Task]) -> list[Task]:
        """Append multiple tasks to the file."""
        try:
            with self.file.open(mode="a") as f:
                for i, task in enumerate(tasks, start=1):
                    f.write(task.to_file())
                    task.i = self.max_task_number + i
        except FileNotFoundError as e:
            raise self.not_found_error from e
        return tasks

    def import_tasks(self):
        """Imports the tasks from the database file."""
        try:
            with self.file.open('r') as f:
                content = f.readlines()
                for i, task in enumerate(content):
                    # Skip empty lines.
                    if task.strip() == "":
                        continue
                    self.task_list.append(Task(i + 1, task.strip()))
        except FileNotFoundError as e:
            raise self.not_found_error() from e

    def __str__(self):
        """List the tasks."""
        s = ""
        for tsk in [ConsoleTask(task.i, task.task_string, self.number_of_digits) for task in self.task_list]:
            s += str(tsk) + "\n"
        return s
