import collections
from typing import List

class Solution:
    def findOrder(self, num_courses: int, prerequisites: List[List[int]]) -> List[int]:
        # Convert prerequisites list to an adjacency list.
        course_dependencies = collections.defaultdict(list)
        for prereq in prerequisites:
            course_dependencies[prereq[0]].append(prereq[1])

        # Keeps track of the suggested course order
        output = []
        # Keeps track of what has been added to the output, O(1) lookup time
        _output = set()
        # Keeps track of course numbers that are currently being evaluated
        # by the digest_course function. Used to detect cycles.
        under_consideration = set()

        def digest_course(course_num: int):
            """
            Updates output. Adds the course to the output if it has no
            dependencies and the course has not yet been added to the output. If
            the course has dependencies, recurses, adding all dependency courses
            to the output before adding the course to the output.

            Returns False if it finds a cycle, indicating that it is not
            possible to satisfy the dependencies for all courses.
            """

            # If this course is already in the output, then there's nothing
            # left to do with this course.
            if course_num in _output:
                return True

            # Record that this course num is currently being evaluated on the
            # call stack.
            under_consideration.add(course_num)

            # Iterate through all dependencies.
            for dep in course_dependencies[course_num]:
                # If the dependency is in "under_consideration", then "dep"
                # is equal to some "course_num" farther up the call stack,
                # indicating a cycle.
                if dep in under_consideration:
                    return False

                # Recurse, ensure the dependency and its dependencies are added
                # to the output. Oh... yeah and check for cycles too.
                if not digest_course(dep):
                    return False

            # At this point, either the course has no dependencies or all of
            # them have been added to the output.
            output.append(course_num)
            _output.add(course_num)

            # No cycles found yet.
            under_consideration.remove(course_num)
            return True

        # Iterate over all course numbers to make sure all courses are added to
        # the output.
        for course_num in range(num_courses):
            if not digest_course(course_num):
                return []

        return output
