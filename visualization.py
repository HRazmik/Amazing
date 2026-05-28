

from maze_gen import Cell, Grid

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

class visualizer:
    def __init__(self,
                 grid: Grid,
                 start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        self.grid = grid
        self.b_matrix: list[list[str]] = []
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end
        for i in range(self.grid.height * 2 + 1):
            temp_arr: list[str] = []
            for j in range(self.grid.width * 2 + 1):
                temp_arr.append(" ")
            self.b_matrix.append(temp_arr)


    def input(self, maze: list[list[int]]) -> None:
        print("ololo", self.grid.height, self.grid.width)
        for i in range(self.grid.height):
            rend_i = i * 2 + 1
            for j in range(self.grid.width):
                rend_j = j * 2 + 1
                if self.grid.north(i, j):
                    self.b_matrix[rend_i - 1][rend_j] = BLOCK
                    if self.grid.west(i,j):
                        self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    elif self.grid.north(i, j - 1):
                        self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    if self.grid.east(i, j):
                        self.b_matrix[rend_i - 1][rend_j + 1] = BLOCK
                    elif self.grid.north(i, j + 1):
                        self.b_matrix[rend_i - 1][rend_j + 1] = BLOCK
                if self.grid.south(i, j):
                    self.b_matrix[rend_i + 1][rend_j] = BLOCK
                    if self.grid.west(i, j):
                        self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK
                    elif self.grid.south(i, j - 1):
                        self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK
                    if self.grid.east(i, j):
                        self.b_matrix[rend_i + 1][rend_j + 1] = BLOCK
                    elif self.grid.south(i, j + 1):
                        self.b_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if self.grid.east(i, j):
                    self.b_matrix[rend_i][rend_j + 1] = BLOCK
                    if self.grid.east(i - 1, j):
                        self.b_matrix[rend_i - 1][rend_j + 1] = BLOCK
                    if self.grid.east(i + 1, j):
                        self.b_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if self.grid.west(i, j):
                    self.b_matrix[rend_i][rend_j - 1] = BLOCK
                    if self.grid.west(i - 1, j):
                        self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    if self.grid.west(i + 1, j):
                        self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK
                # if self.grid.get & 0xf == 15:
                #     self.b_matrix[rend_i][rend_j] = BLOCK


    def draw(self, wall_colour: str, ft_colour: str) -> None:
        GREEN = "\033[0;32m"
        RED = "\033[0;31m"
        BLUE = "\033[0;34m"
        BOLD_YELLOW = "\033[1;33m"
        BG_RED = "\033[41m"  # Background color
        RESET = "\033[0m"
        p42: list[list[int]] = [
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
        print(wall_colour, end='')
        for i in range(self.grid.height * 2 + 1):
            for j in range(self.grid.width * 2 + 1):
                center_i = (self.grid.height * 2 + 1) // 2 - 1
                center_j = (self.grid.width * 2 + 1) // 2
                char = self.b_matrix[i][j]
                # if i >= center_i - 5 and i <= center_i + 5:
                #     if j >= center_j - 7 and j <= center_j + 8:
                #         if p42[i - (center_i - 5)][j - (center_j - 7)]:
                #             print(ft_colour, end='')
                #         else:
                #             print(wall_colour, end='')
                # if i == self.start[0] * 2 + 1 and j == self.start[1] * 2 + 1:
                #     char = "\033[41m" + char + RESET + wall_colour
                # if i == self.end[0] * 2 + 1 and j == self.end[1] * 2 + 1:
                #     char = "\033[44m" + char + RESET + wall_colour
                print(char, end='')
                print(char, end='')
            print()
        print(RESET, end='')


matrixxx = Grid(8, 2)
matrixxx.generate()


output = visualizer(matrixxx, (19, 20), (7, 18))
output.input(matrix)
output.draw("\033[1;92m", "\033[;36m")
