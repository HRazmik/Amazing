from maze_gen import Grid


def dfs_path(grid: Grid,
             start: tuple[int, int],
             goal: tuple[int, int]
             ) -> list[tuple[int, int]]:
    si, sj = start
    gi, gj = goal

    visited = [[False for _ in range(grid.width)] for _ in range(grid.height)]
    parent = {}

    def dfs_rec(i: int, j: int) -> bool:
        visited[i][j] = True
        if (i, j) == (gi, gj):
            return True

        for ni, nj in grid.get_neighbour(i, j):
            if not visited[ni][nj]:
                parent[(ni, nj)] = (i, j)
                if dfs_rec(ni, nj):
                    return True

        return False
    found = dfs_rec(si, sj)
    if not found:
        return []

    curr = (gi, gj)
    path = []

    while curr != ((si, sj)):
        path.append(curr)
        curr = parent[curr]

    path.append((si, sj))
    path.reverse()
    str_path = ""
    for i in range (len(path) - 1):
        ci, cj = path[i]
        ni, nj = path[i + 1]
        if ni < ci:
            str_path += "N"
        elif ni > ci:
            str_path += "S"
        elif nj < cj:
            str_path += "W"
        else:
            str_path += "E"
    print (str_path)
    return path
