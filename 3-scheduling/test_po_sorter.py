from typing import List

import pytest
from po_sorter import load_po_file, task_from_str, verify_sort
from task import Task

TEST_FILES_PATH = "3-scheduling/"


@pytest.fixture
def sorted_tasks() -> List[Task]:
    return [
        Task("A", 0, []),
        Task("B", 1, [0]),
        Task("C", 2, [0, 1]),
    ]


def test_verify_sort(sorted_tasks):
    assert verify_sort(sorted_tasks)


def test_verify_sort_returns_false_if_the_list_is_not_properly_sorted():
    assert not verify_sort([Task("A", 0, [1])])


def test_parse_line():
    task = task_from_str("18, Finish dungeon, [13, 14]")
    assert task.name == "Finish dungeon"
    assert task.index == 18
    assert task.prereq_numbers == [13, 14]


def test_parse_line_with_no_prerequisites():
    task = task_from_str("1, Grade site, []")
    assert task.name == "Grade site"
    assert task.index == 1
    assert task.prereq_numbers == []


def test_load_po_file():
    po_sorter = load_po_file(TEST_FILES_PATH + "castle.po")
    assert len(po_sorter.tasks) == 29
    assert po_sorter.tasks[0].prereq_tasks[0].name == "Install siding"
