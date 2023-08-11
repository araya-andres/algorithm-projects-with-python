from typing import List

import pytest
from task import Task


@pytest.fixture
def sorted_tasks() -> List[Task]:
    tasks = [
        Task("A", index=0, prereq_numbers=[], duration=1),
        Task("B", index=1, prereq_numbers=[0], duration=1),
        Task("C", index=2, prereq_numbers=[0, 1], duration=1),
    ]
    for task in tasks:
        task.numbers_to_tasks(tasks)
    return tasks


@pytest.fixture
def independent_tasks() -> List[Task]:
    return [
        Task("A", index=0, prereq_numbers=[], duration=1),
        Task("B", index=1, prereq_numbers=[], duration=1),
    ]
