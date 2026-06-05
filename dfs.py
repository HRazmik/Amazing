from maze_gen import Grid
from collections import deque


def dfs_path(grid: Grid,
             start: tuple[int, int],
             goal: tuple[int, int]
             ) -> list[tuple[int, int]]:
    si, sj = start
    gi, gj = goal

    grid.set_beck()

    queue = deque()
    parent = {}

    queue.append((si, sj))
    grid.cells[si][sj].visit()

    while queue:
        i, j = queue.popleft()

        if (i, j) == (gi, gj):
            break

        for ni, nj in grid.get_neighbour(i, j):
            if not grid.cells[ni][nj].visited:
                grid.cells[ni][nj].visit()
                parent[(ni, nj)] = (i, j)
                queue.append((ni, nj))

    if (gi, gj) not in parent and (si, sj) != (gi, gj):
        return []

    curr = (gi, gj)
    path = []

    while curr != (si, sj):
        path.append(curr)
        curr = parent[curr]
    path.append((si, sj))
    path.reverse()
    return path


def path_to_str(path: list[tuple[int, int]]) -> str:
    path_str: str = ""
    for i in range(len(path) - 1):
        if path[i][0] < path[i + 1][0]:
            path_str += "S"
        elif path[i][0] > path[i + 1][0]:
            path_str += "N"
        elif path[i][1] < path[i + 1][1]:
            path_str += "E"
        else:
            path_str += "W"
    return path_str
