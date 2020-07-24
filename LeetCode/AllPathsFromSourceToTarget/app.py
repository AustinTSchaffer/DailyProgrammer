from typing import List

class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        target = len(graph) - 1
        path = []
        results = []

        def _recurse(node: int):
            if node == target:
                results.append([*path, target])
                return

            path.append(node)

            for edge in graph[node]:
                _recurse(edge)

            del path[-1]

        _recurse(0)

        return results


if __name__ == "__main__":
    s = Solution()
    input_ = [[1,2], [3], [3], []]
    result = s.allPathsSourceTarget(input_)
    print(result)
