from task import Task


def test_task_to_str():
    task_name = "Dig dungeon"
    task = Task(task_name, 1, [], 1)
    assert str(task) == task_name


def test_numbers_to_tasks():
    task_a = Task("Grade site", 0, [], 1)
    task_b = Task("Dig dungeon", 1, [0], 1)
    tasks = [task_a, task_b]

    task_a.numbers_to_tasks(tasks)
    assert task_a.prereq_tasks == []

    task_b.numbers_to_tasks(tasks)
    assert task_b.prereq_tasks == [task_a]
