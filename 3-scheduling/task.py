from __future__ import annotations

from typing import List


class Task:
    def __init__(self, name: str, index: int, prereq_numbers: List[int]):
        self.name = name
        self.index = index
        self.prereq_numbers = prereq_numbers
