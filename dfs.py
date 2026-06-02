from maze_gen import Grid, Cell
from collections import deque

def dfs_path(grid, start, goal):
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