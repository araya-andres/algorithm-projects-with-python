from __future__ import annotations

from typing import List


class Task:
    def __init__(self, name: str, index: int, prereq_numbers: List[int]):
        self.name: str = name
        self.index: int = index
        self.prereq_numbers: List[int] = prereq_numbers
        self.prereq_tasks: List[Task] = []

    def __str__(self) -> str:
        return self.name

    def numbers_to_tasks(self, tasks: List[Task]) -> None:
        self.prereq_tasks = [tasks[index] for index in self.prereq_numbers]
