from __future__ import annotations

import tkinter as tk
from typing import List

from task import Task

TEXT_WIDTH = 100
TEXT_HEIGHT = 10

DAY_WIDTH = TEXT_HEIGHT

TASK_HEIGHT = 6


def _arrange_tasks_boxes(columns: List[List[Task]], x_min: float, y_min: float):
    pass


def _draw_grid(
    canvas: tk.Canvas,
    x_min: float,
    y_min: float,
    no_rows: int,
    no_cols: int,
):
    pass


def _draw_links(canvas: tk.Canvas, columns: List[List[Task]]):
    pass


def _draw_tasks_boxes(canvas: tk.Canvas, columns: List[List[Task]]):
    pass


def _draw_tasks_text(canvas: tk.Canvas, tasks: List[Task], x_min: float, y_min: float):
    pass


def draw(canvas: tk.Canvas, tasks: List[Task], columns: List[List[Task]]) -> None:
    """
    Draw a PERT chart.
    """
    x_min = y_min = 10
    _arrange_tasks_boxes(columns, x_min=x_min + TEXT_WIDTH, y_min=y_min + TEXT_HEIGHT)
    _draw_grid(
        canvas,
        x_min=x_min + TEXT_WIDTH,
        y_min=y_min,
        no_rows=len(tasks),
        no_cols=len(columns),
    )
    _draw_links(canvas, columns)
    _draw_tasks_text(canvas, tasks, x_min=x_min, y_min=y_min + TEXT_HEIGHT)
    _draw_tasks_boxes(canvas, columns)
