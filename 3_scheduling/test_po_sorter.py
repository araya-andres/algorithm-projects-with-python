from typing import List

import po_sorter
from task import Task
from test_fixtures import independent_tasks, sorted_tasks

TEST_FILES_PATH = "3_scheduling/test_files/"


def test_verify_sort(sorted_tasks):
    assert po_sorter.verify_sort(sorted_tasks)


def test_verify_sort_returns_false_if_the_list_is_not_properly_sorted():
    assert not po_sorter.verify_sort([Task("A", 0, [1], 1)])


def test_parse_line():
    task = po_sorter.task_from_str("18, 1, Finish dungeon, [13, 14]")
    assert task.name == "Finish dungeon"
    assert task.index == 18
    assert task.prereq_numbers == [13, 14]
    assert task.duration == 1


def test_parse_line_with_no_prerequisites():
    task = po_sorter.task_from_str("1, 2, Grade site, []")
    assert task.name == "Grade site"
    assert task.index == 1
    assert task.prereq_numbers == []
    assert task.duration == 2


def test_load_po_file():
    tasks = po_sorter.load_po_file(TEST_FILES_PATH + "castle.po")
    assert len(tasks) == 31
    assert tasks[1].prereq_tasks[0].name == "Install siding"


def test_topo_sort():
    tasks = [
        Task("A", index=0, prereq_numbers=[1, 2], duration=1),
        Task("B", index=1, prereq_numbers=[2], duration=1),
        Task("C", index=2, prereq_numbers=[], duration=1),
    ]
    for task in tasks:
        task.numbers_to_tasks(tasks)
    sorted_tasks = po_sorter.topo_sort(tasks)
    assert sorted_tasks[0].name == "C"
    assert sorted_tasks[1].name == "B"
    assert sorted_tasks[2].name == "A"
    assert po_sorter.verify_sort(sorted_tasks)


def test_topo_sort_with_a_sorted_list(sorted_tasks: List[Task]):
    assert po_sorter.verify_sort(po_sorter.topo_sort(sorted_tasks))


def test_topo_sort_with_independet_tasks(independent_tasks: List[Task]):
    assert po_sorter.verify_sort(po_sorter.topo_sort(independent_tasks))


def test_topo_sort_with_an_empty_list():
    assert po_sorter.verify_sort(po_sorter.topo_sort([]))


def test_topo_sort_with_loop():
    tasks = po_sorter.load_po_file(TEST_FILES_PATH + "impossible.po")
    sorted_tasks = po_sorter.topo_sort(tasks)
    assert len(sorted_tasks) == 3


def test_build_pert_chart(sorted_tasks: List[Task]):
    columns = po_sorter.build_pert_chart(sorted_tasks)
    assert len(columns) == 3
    assert all(len(rows) == 1 for rows in columns)
    assert columns[0][0].name == "A"
    assert columns[1][0].name == "B"
    assert columns[2][0].name == "C"


def test_build_pert_chart_with_independent_tasks(independent_tasks: List[Task]):
    columns = po_sorter.build_pert_chart(independent_tasks)
    assert len(columns) == 1
    assert len(columns[0]) == 2


def test_build_pert_chart_with_an_empty_list():
    columns = po_sorter.build_pert_chart([])
    assert len(columns) == 0


def test_set_time():
    tasks = [
        Task("A", index=0, prereq_numbers=[], duration=2),
        Task("B", index=1, prereq_numbers=[], duration=1),
        Task("C", index=2, prereq_numbers=[0, 1], duration=1),
    ]
    for task in tasks:
        task.numbers_to_tasks(tasks)
        task.set_times()
    assert tasks[-1].start_time == 2


def test_end_time(sorted_tasks: List[Task]):
    for task in sorted_tasks:
        task.set_times()
    assert sorted_tasks[0].end_time() == 1
    assert sorted_tasks[1].end_time() == 2
    assert sorted_tasks[2].end_time() == 3
