from maze_gen import Grid, Cell
from collections import deque


def get_neighbour(grid: Grid, i: int, j: int) -> list[tuple[int, int]]:
    neighbour: list[tuple[int, int]] = []
    cell: Cell = grid.cells[i][j]
    if i > 0 and not (cell.walls & 0x1):
        neighbour.append((i - 1, j))
    if j < grid.width - 1 and not (cell.walls & 0x2):
        neighbour.append((i, j + 1))
    if i < grid.height - 1 and not (cell.walls & 0x4):
        neighbour.append((i + 1, j))
    if j > 0 and not (cell.walls & 0x8):
        neighbour.append((i, j - 1))
    return neighbour


def dfs_path(grid: Grid,
             start: tuple[int, int],
             goal: tuple[int, int]
             ) -> list[tuple[int, int]]:
    """
    Find a path in the maze from start to goal using Breadth-First Search(BFS).

    This function uses BFS to ensure the shortest path
    in an unweighted maze.

    Args:
        grid (Grid): Maze grid containing cells and wall structure.
        start (tuple[int, int]): Starting coordinates (row, col).
        goal (tuple[int, int]): Goal coordinates (row, col).

    Returns:
        list[tuple[int, int]]: List of coordinates representing the path from
        start to goal. Returns an empty list if no path exists.
    """

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

        for ni, nj in get_neighbour(grid, i, j):
            if not grid.cells[ni][nj].visited:
                grid.cells[ni][nj].visit()
                parent[(ni, nj)] = (i, j)
                queue.append((ni, nj))

    if (gi, gj) not in parent and (si, sj) != (gi, gj):
        print(100001)
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
    """
    Convert a path (list of coordinates) into a string of directions.

    Directions are encoded as:
        N = move up
        S = move down
        E = move right
        W = move left

    Args:
        path (list[tuple[int, int]]): Path as a list of (row, col) coordinates.

    Returns:
        str: String representing movement directions along the path.
    """

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
