from __future__ import annotations

import tkinter as tk
from typing import List

from po_sorter import is_link_critical_to_project, is_link_critical_to_task
from task import Task

X_SPACING = 50
Y_SPACING = 50
SIDE = 50
HALF_SIDE = 25


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
                if is_link_critical_to_task(task, follower):
                    width = 3
                    if is_link_critical_to_project(task, follower):
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


def draw(canvas: tk.Canvas, columns: List[List[Task]]) -> None:
    """
    Draw a PERT chart.
    """
    _arrange_tasks(columns)
    _draw_links(canvas, columns)
    _draw_tasks(canvas, columns)
