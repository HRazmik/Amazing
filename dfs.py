from maze_gen import Cell, Grid
import visualization


def dfs_path(grid, start, goal) -> list[tuple[int, int]]:
    si,sj = start
    gi,gj = goal

    visited = [[False for _ in range(grid.width)] for _ in range(grid.height)]
    parent = {}

    def dfs_rec(i: int, j: int) -> bool:
        visited[i][j] = True
        if (i,j) == (gi, gj):
            return True

        for ni,nj in grid.get_neighbour(i, j):
            if not visited[ni][nj]:
                parent[(ni, nj)] = (i,j)
                if dfs_rec(ni, nj):
                    return True
        return False
    found = dfs_rec(si,sj)

    if not found:
        return []

    curr = (gi, gj)
    path = []

    while curr != ((si, sj)):
        path.append(curr)
        curr = parent[curr]

    path.append((si, sj))
    path.reverse()

    return path

# grid = Grid(20, 20)
# grid.generate()
# grid.add_pattern()

# path = dfs_path(grid, (1, 1), (19, 14))
# print(path)

met = Grid(25, 20)
met.generate()
rows = [
    "9515391539551795151151153",
    "EBABAE812853C1412BA812812",
    "96A8416A84545412AC4282C2A",
    "C3A83816A9395384453A82D02",
    "96842A852AC07AAD13A8283C2",
    "C1296C43AAB83AA92AA8686BA",
    "92E853968428444682AC12902",
    "AC3814452FA83FFF92C52C42A",
    "85684117AFC6857FBC1383D06",
    "C53AD043AFFFAFFF856AA8143",
    "91441294297FAFD501142C6BA",
    "AA912AC3843FAFFF82856D52A",
    "842A8692A92B8517C4451552A",
    "816AC384468285293917A9542",
    "C416928513C443A828456C3BA",
    "91416AA92C393A82801553AAA",
    "A81292AA814682C6A8693C6AA",
    "A8442C6C2C1168552C16A9542",
    "86956951692C1455416928552",
    "C545545456C54555545444556",
]

matrix = [[int(c, 16) for c in row] for row in rows]
met.change_grid(matrix)

path = dfs_path(met, (1,4), (8,14))
met = visualization.visualizer(met, (1,4), (8,14), path)
met.input()
met.draw("\033[1;93m", "\033[;36m")





