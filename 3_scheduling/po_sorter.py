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
    pattern = re.compile(r"""(\d+),\s*(\d+),\s*([^,]*),\s*\[([^\]]*)]""")
    match = pattern.match(line)
    index = int(match.group(1))
    duration = int(match.group(2))
    name = match.group(3)
    prereq_numbers = [int(index) for index in match.group(4).split(",") if index]
    return Task(name, index, prereq_numbers, duration)


def load_po_file(filename: str) -> List[Task]:
    """
    Load a .po file
    """
    tasks: List[Task] = []
    with open(filename, mode="r", encoding="utf-8") as reader:
        while line := reader.readline():
            tasks.append(task_from_str(line.strip()))
    for task in tasks:
        task.numbers_to_tasks(tasks)
    return tasks


def topo_sort(tasks: List[Task]) -> List[Task]:
    """
    Perform topological sorting.
    """
    _prepare(tasks)
    sorted_tasks: List[Task] = []
    ready_tasks: List[Task] = [task for task in tasks if task.prereq_count == 0]
    while ready_tasks:
        task = ready_tasks.pop(0)
        for follower in task.followers:
            follower.prereq_count -= 1
            if follower.prereq_count == 0:
                ready_tasks.append(follower)
        sorted_tasks.append(task)
    return _update_indexes(sorted_tasks)


def build_pert_chart(tasks: List[Task]) -> List[List[Task]]:
    """
    Build a pert chart
    """
    if not tasks:
        return []
    _prepare(tasks)
    ready_tasks: List[Task] = [task for task in tasks if task.prereq_count == 0]
    new_ready_tasks: List[Task] = []
    columns: List[List[Task]] = [list(ready_tasks)]
    while ready_tasks:
        task = ready_tasks.pop(0)
        task.set_times()
        for follower in task.followers:
            follower.prereq_count -= 1
            if follower.prereq_count == 0:
                new_ready_tasks.append(follower)
        if not ready_tasks and new_ready_tasks:
            ready_tasks = new_ready_tasks
            new_ready_tasks = []
            columns.append(list(ready_tasks))
    last_task(columns).mark_is_critical()
    return columns


def is_link_critical_to_project(task: Task, follower: Task) -> bool:
    return task.is_critical and follower.is_critical


def is_link_critical_to_task(task: Task, follower: Task) -> bool:
    return task.end_time() == follower.start_time


def last_task(columns: List[List[Task]]) -> Task:
    last = None
    end_time = 0
    for task in columns[-1]:
        if task.end_time() > end_time:
            last = task
            end_time = task.end_time()
    return last


def _prepare(tasks: List[Task]):
    for task in tasks:
        task.prereq_count = len(task.prereq_tasks)
        task.is_critical = False
        for prereq in task.prereq_tasks:
            prereq.followers.append(task)


def _update_indexes(tasks: List[Task]) -> List[Task]:
    for i, task in enumerate(tasks):
        task.index = i
        task.followers = []
    for task in tasks:
        task.prereq_numbers = [prereq.index for prereq in task.prereq_tasks]
    return tasks
