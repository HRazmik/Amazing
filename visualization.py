BLOCK = "\u2588"
SPACE = " "
rows = [
    "9515391539551795151151153",
    "EBABAE812853C1412BA812812",
    "96A8416A84545412AC4282C2A",
    "C3A83816A9395384453A82D02",
    "96842A852AC07AAD13A8283C2",
    "C1296C43AAB83AA92AA8686BA",
    "92E853968428444682AC12902",
    "AC3814452FA83FFF82C52C42A",
    "85684117AFC6857FAC1383D06",
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


def north(cell):
    return bool(cell & 0x1)


def east(cell):
    return bool(cell & 0x2)


def south(cell):
    return bool(cell & 0x4)


def west(cell):
    return bool(cell & 0x8)


class visualizer:
    def __init__(self, height: int = -1, width: int = -1) -> None:
        self.width: int = width
        self.height: int = height
        self.block_matrix: list[list[str]] = \
            [[" " for i in range(self.width * 2 + 1)] for i in range(self.height * 2 + 1)]

    def input(self, maze: list[list[int]]) -> None:
        for i in range(self.height):
            for j in range(self.width):
                rend_i = i * 2 + 1
                rend_j = j * 2 + 1
                if north(maze[i][j]):
                    self.block_matrix[rend_i - 1][rend_j] = BLOCK
                    if j - 1 >= 0 and north(maze[i][j - 1]):
                        self.block_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    if j + 1 < self.width and north(maze[i][j + 1]):
                        self.block_matrix[rend_i - 1][rend_j + 1] = BLOCK
                    if west(maze[i][j]):
                        self.block_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    if east(maze[i][j]):
                        self.block_matrix[rend_i - 1][rend_j + 1] = BLOCK
                if south(maze[i][j]):
                    self.block_matrix[rend_i + 1][rend_j] = BLOCK
                    if j - 1 >= 0 and south(maze[i][j - 1]):
                        self.block_matrix[rend_i + 1][rend_j - 1] = BLOCK
                    if j + 1 < self.width and south(maze[i][j + 1]):
                        self.block_matrix[rend_i + 1][rend_j + 1] = BLOCK
                    if west(maze[i][j]):
                        self.block_matrix[rend_i + 1][rend_j - 1] = BLOCK
                    if east(maze[i][j]):
                        self.block_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if east(maze[i][j]):
                    self.block_matrix[rend_i][rend_j + 1] = BLOCK
                    if i - 1 >= 0 and east(maze[i - 1][j]):
                        self.block_matrix[rend_i - 1][rend_j + 1] = BLOCK
                    if i + 1 < self.height and east(maze[i + 1][j]):
                        self.block_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if west(maze[i][j]):
                    self.block_matrix[rend_i][rend_j - 1] = BLOCK
                    if i - 1 >= 0 and west(maze[i - 1][j]):
                        self.block_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    if i + 1 < self.height and west(maze[i + 1][j]):
                        self.block_matrix[rend_i + 1][rend_j - 1] = BLOCK

    def draw(self):
        for line in self.block_matrix:
            i = 1
            for char in line:
                i += 1
                print(char, end='')
                print(char, end='')
            print()

output = visualizer(len(matrix), len(matrix[0]))
output.input(matrix)
output.draw()
