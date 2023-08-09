from __future__ import annotations

from typing import List


class Task:
    def __init__(self, name: str, index: int, prereq_numbers: List[int], duration: int):
        self.name: str = name
        self.index: int = index
        self.prereq_numbers: List[int] = prereq_numbers
        self.duration: int = duration
        self.prereq_tasks: List[Task] = []
        self.prereq_count: int = 0
        self.followers: List[Task] = []
        self.is_critical = False
        self.start_time = 0

    def __str__(self) -> str:
        return self.name

    def end_time(self) -> int:
        return self.start_time + self.duration

    def mark_is_critical(self) -> None:
        self.is_critical = True

    def numbers_to_tasks(self, tasks: List[Task]) -> None:
        self.prereq_tasks = [tasks[index] for index in self.prereq_numbers]

    def set_times(self) -> None:
        if self.prereq_tasks:
            self.start_time = max(prereq.end_time() for prereq in self.prereq_tasks)
        else:
            self.start_time = 0
