from __future__ import annotations

import tkinter as tk
from typing import List

from po_sorter import is_link_critical_to_project, is_link_critical_to_task
from task import Task

MARGIN = 5
TEXT_HEIGHT = 20
TEXT_WIDTH = 130
TASK_HEIGHT = TEXT_HEIGHT
BOX_HEIGHT = TASK_HEIGHT - 2 * MARGIN
DAY_WIDTH = TEXT_HEIGHT


def _arrange_tasks_boxes(tasks: List[Task], x_min: float, y_min: float):
    for i, task in enumerate(tasks):
        x0 = x_min + task.start_time * DAY_WIDTH
        y0 = y_min + i * TASK_HEIGHT + MARGIN
        x1 = x0 + task.duration * DAY_WIDTH
        y1 = y0 + BOX_HEIGHT
        task.bounds = (x0, y0, x1, y1)
        task.anchor_w = (x0, (y0 + y1) / 2)
        task.anchor_e = (x1, (y0 + y1) / 2)


def _draw_grid(
    canvas: tk.Canvas,
    x_min: float,
    y_min: float,
    no_rows: int,
    no_cols: int,
):
    color = "gray95"

    x = x_min
    y0 = y_min
    y1 = y_min + TEXT_HEIGHT * (no_rows + 1)
    for _ in range(no_cols + 1):
        canvas.create_line(x, y0, x, y1, fill=color)
        x += DAY_WIDTH

    y = y_min
    x0 = x_min
    x1 = x_min + DAY_WIDTH * no_cols
    for _ in range(no_rows + 2):
        canvas.create_line(x0, y, x1, y, fill=color)
        y += TEXT_HEIGHT

    x = x_min + DAY_WIDTH / 2
    y = y_min + TEXT_HEIGHT / 2
    for i in range(no_cols):
        canvas.create_text(
            x, y, fill="SpringGreen2", font=("arial", 8), text=str(i + 1)
        )
        x += DAY_WIDTH


def _draw_links(canvas: tk.Canvas, tasks: List[Task]):
    for task in tasks:
        x1, y1 = task.anchor_w
        for prereq in task.prereq_tasks:
            fill = "black"
            width = 1
            if is_link_critical_to_task(prereq, task):
                width = 3
                if is_link_critical_to_project(prereq, task):
                    fill = "red"
            x1 += MARGIN
            x0, y0 = prereq.anchor_e
            sign = -1 if prereq.index < task.index else 1
            canvas.create_line(x0, y0, x1, y0, fill=fill, width=width)
            canvas.create_line(
                x1,
                y0,
                x1,
                y1 + sign * BOX_HEIGHT / 2,
                arrow=tk.LAST,
                fill=fill,
                width=width,
            )


def _draw_tasks_boxes(canvas: tk.Canvas, tasks: List[Task]):
    for task in tasks:
        if task.is_critical:
            outline = "red"
            fill = "pink"
        else:
            outline = "black"
            fill = "lightblue"
        canvas.create_rectangle(*task.bounds, fill=fill, outline=outline)


def _draw_tasks_text(canvas: tk.Canvas, tasks: List[Task], x_min: float, y_min: float):
    y = y_min + TEXT_HEIGHT / 2
    for task in tasks:
        text = f"{task.index}. {task.name}"
        canvas.create_text(x_min, y, text=text, anchor=tk.W)
        y += TEXT_HEIGHT


def draw(canvas: tk.Canvas, tasks: List[Task]) -> None:
    """
    Draw a Grantt chart.
    """
    x_min = y_min = 10
    _arrange_tasks_boxes(tasks, x_min=x_min + TEXT_WIDTH, y_min=y_min + TEXT_HEIGHT)
    _draw_grid(
        canvas,
        x_min=x_min + TEXT_WIDTH,
        y_min=y_min,
        no_rows=len(tasks),
        no_cols=max(task.end_time() for task in tasks),
    )
    _draw_tasks_text(canvas, tasks, x_min=x_min, y_min=y_min + TEXT_HEIGHT)
    _draw_links(canvas, tasks)
    _draw_tasks_boxes(canvas, tasks)
