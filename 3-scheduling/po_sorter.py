from __future__ import annotations

import re
from typing import List

from task import Task


def verify_sort(sorted_tasks: List[Task]) -> bool:
    """
    For each task in sorted_tasks, verify that the pre-requisites are at an index less
    than the current task index.
    """
    for i, task in enumerate(sorted_tasks):
        if any(i <= prereq_number for prereq_number in task.prereq_numbers):
            return False
    return True


def task_from_str(line: str) -> Task:
    """
    Parse a line from a .po file
    """
    pattern = re.compile(r"""(\d*), *([^,]*), *\[([^\]]*)]""")
    match = pattern.match(line)
    index = int(match.group(1))
    name = match.group(2)
    prereq_numbers = [int(index) for index in match.group(3).split(",") if index]
    return Task(name, index, prereq_numbers)


def load_po_file(filename: str) -> PoSorter:
    """
    Load a .po file
    """
    tasks: List[Task] = []
    with open(filename, mode="r", encoding="utf-8") as reader:
        while line := reader.readline():
            tasks.append(task_from_str(line.strip()))
    for task in tasks:
        task.numbers_to_tasks(tasks)
    return PoSorter(tasks)


class PoSorter:
    def __init__(self, tasks: List[Task]):
        self.tasks: List[Task] = tasks
        self.sorted_tasks: List[Task] = []

    def topo_sort(self):
        pass
