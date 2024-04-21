from typing import Tuple

import click

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.DoneFileNotFoundError import DoneFileNotFoundError
from todotree.Task.DoneTask import DoneTask
from todotree.Task.Task import Task


class AddX(AbstractCommand):

    def run(self, task: Tuple):
        done = DoneTask.task_to_done(Task(0, " ".join(map(str, task))))
        if not self.config.paths.done_file.exists():
            DoneFileNotFoundError("").echo_and_exit(self.config)
        with self.config.paths.done_file.open("a") as f:
            f.write(done.to_file())
        click.echo(done)
