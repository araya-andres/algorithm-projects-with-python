from typing import List

import pert_chart
import po_sorter
from pert_chart import HALF_SIDE, X_SPACING, Y_SPACING
from task import Task
from test_fixtures import independent_tasks, sorted_tasks


def test_arrange_tasks_horizontal(sorted_tasks: List[Task]):
    columns = po_sorter.build_pert_chart(sorted_tasks)
    pert_chart._arrange_tasks(columns, x_min=0, y_min=0)
    columns[0][0].center == (HALF_SIDE, HALF_SIDE)
    columns[1][0].center == (3 * HALF_SIDE + X_SPACING, HALF_SIDE)
    columns[2][0].center == (5 * HALF_SIDE + 2 * X_SPACING, HALF_SIDE)


def test_arrange_tasks_vertical(independent_tasks: List[Task]):
    columns = po_sorter.build_pert_chart(independent_tasks)
    pert_chart._arrange_tasks(columns, x_min=0, y_min=0)
    columns[0][0].center == (HALF_SIDE, HALF_SIDE)
    columns[0][1].center == (HALF_SIDE, 3 * HALF_SIDE + Y_SPACING)
