from typing import List

import po_sorter
import pytest
from task import Task

TEST_FILES_PATH = "3-scheduling/test-files/"


@pytest.fixture
def sorted_tasks() -> List[Task]:
    tasks = [
        Task("A", 0, []),
        Task("B", 1, [0]),
        Task("C", 2, [0, 1]),
    ]
    for task in tasks:
        task.numbers_to_tasks(tasks)
    return tasks


def test_verify_sort(sorted_tasks):
    assert po_sorter.verify_sort(sorted_tasks)


def test_verify_sort_returns_false_if_the_list_is_not_properly_sorted():
    assert not po_sorter.verify_sort([Task("A", 0, [1])])


def test_parse_line():
    task = po_sorter.task_from_str("18, Finish dungeon, [13, 14]")
    assert task.name == "Finish dungeon"
    assert task.index == 18
    assert task.prereq_numbers == [13, 14]


def test_parse_line_with_no_prerequisites():
    task = po_sorter.task_from_str("1, Grade site, []")
    assert task.name == "Grade site"
    assert task.index == 1
    assert task.prereq_numbers == []


def test_load_po_file():
    tasks = po_sorter.load_po_file(TEST_FILES_PATH + "castle.po")
    assert len(tasks) == 29
    assert tasks[0].prereq_tasks[0].name == "Install siding"


def test_topo_sort():
    tasks = [
        Task("A", 0, [1, 2]),
        Task("B", 1, [2]),
        Task("C", 2, []),
    ]
    for task in tasks:
        task.numbers_to_tasks(tasks)
    sorted_tasks = po_sorter.topo_sort(tasks)
    assert sorted_tasks[0].name == "C"
    assert sorted_tasks[1].name == "B"
    assert sorted_tasks[2].name == "A"
    assert po_sorter.verify_sort(sorted_tasks)


def test_topo_sort_with_a_sorted_list(sorted_tasks):
    assert po_sorter.verify_sort(po_sorter.topo_sort(sorted_tasks))


def test_topo_sort_with_loop():
    tasks = po_sorter.load_po_file(TEST_FILES_PATH + "impossible.po")
    sorted_tasks = po_sorter.topo_sort(tasks)
    assert len(sorted_tasks) == 3


def test_build_pert_chart(sorted_tasks):
    columns = po_sorter.build_pert_chart(sorted_tasks)
    assert len(columns) == 3
    assert all(len(row) == 1 for row in columns)
    assert columns[0][0].name == "A"
    assert columns[1][0].name == "B"
    assert columns[2][0].name == "C"
