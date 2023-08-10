from __future__ import annotations

import re
import tkinter as tk
from typing import List

from task import Task

X_SPACING = 50
Y_SPACING = 50
SIDE = 50
HALF_SIDE = 25


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
    _last_task(columns).mark_is_critical()
    return columns


def _arrange_tasks(columns: List[List[Task]], x_min: float = 10, y_min: float = 10):
    _x = x_min
    for rows in columns:
        _y = y_min
        for task in rows:
            task.bounds = (_x, _y, _x + SIDE, _y + SIDE)
            task.center = (_x + HALF_SIDE, _y + HALF_SIDE)
            _y += SIDE + Y_SPACING
        _x += SIDE + X_SPACING


def _draw_links(canvas: tk.Canvas, columns: List[List[Task]]):
    for rows in columns:
        for task in rows:
            _x0 = task.center[0] + HALF_SIDE
            _y0 = task.center[1]
            for follower in task.followers:
                fill = "black"
                width = 1
                if _is_link_critical_to_task(task, follower):
                    width = 3
                    if _is_link_critical_to_project(task, follower):
                        fill = "red"
                _x1 = follower.center[0] - HALF_SIDE
                _y1 = follower.center[1]
                canvas.create_line(
                    _x0, _y0, _x1, _y1, arrow=tk.LAST, fill=fill, width=width
                )


def _draw_tasks(canvas: tk.Canvas, columns: List[List[Task]]):
    for rows in columns:
        for task in rows:
            if task.is_critical:
                color = "red"
                fill = "pink"
            else:
                color = "black"
                fill = "lightblue"
            text = "Task {}\nDur: {}\nStart:{}\nEnd:{}".format(
                task.index, task.duration, task.start_time, task.end_time()
            )
            canvas.create_rectangle(task.bounds, fill=fill, outline=color)
            canvas.create_text(
                *task.center, fill=color, font=("arial", 7), justify="center", text=text
            )


def draw_pert_chart(canvas: tk.Canvas, columns: List[List[Task]]):
    """
    Draw a PERT chart.
    """
    _arrange_tasks(columns)
    _draw_links(canvas, columns)
    _draw_tasks(canvas, columns)


def _is_link_critical_to_project(task: Task, follower: Task) -> bool:
    return task.is_critical and follower.is_critical


def _is_link_critical_to_task(task: Task, follower: Task) -> bool:
    return task.end_time() == follower.start_time


def _last_task(columns: List[List[Task]]):
    return columns[-1][0]  # FIXME


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
