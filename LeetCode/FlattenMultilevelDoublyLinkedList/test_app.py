import unittest

import app

def test_tree_1() -> app._Node:
    level_1 = app.generate_branch([1, 2, 3, 4, 5, 6])
    level_2 = app.generate_branch([7, 8, 9, 10])
    level_3 = app.generate_branch([11, 12])

    level_1.next.next.child = level_2
    level_2.next.child = level_3

    return level_1

def test_tree_2() -> app._Node:
    level_1 = app.generate_branch([1, 2])
    level_2 = app.generate_branch([3])
    level_1.child = level_2

    return level_1

def test_tree_3() -> app._Node:
    return None

def test_tree_4() -> app._Node:
    head = None
    prev = None
    for i in range(10):
        curr = app._Node(i)
        if not head:
            head = curr
        if prev:
            prev.child = curr
        prev = curr
    return head
