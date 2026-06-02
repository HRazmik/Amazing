from maze_gen import Cell, Grid

BLOCK = "\u2588"
SPACE = " "

class visualizer:
    def __init__(self,
                 grid: Grid,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 path: list[tuple[int, int]]
                 ) -> None:
        self.path = path
        self.grid = grid
        self.b_matrix: list[list[str]] = []
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end
        for i in range(self.grid.height * 2 + 1):
            temp_arr: list[str] = []
            for j in range(self.grid.width * 2 + 1):
                temp_arr.append(" ")
            self.b_matrix.append(temp_arr)

    def input(self) -> None:
        for i in range(self.grid.height):
            rend_i = i * 2 + 1
            for j in range(self.grid.width):
                rend_j = j * 2 + 1
                if i == 0 and self.grid.north(i, j):
                    self.b_matrix[rend_i - 1][rend_j] = BLOCK
                    self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i - 1][rend_j + 1] = BLOCK
                if self.grid.east(i, j):
                    self.b_matrix[rend_i][rend_j + 1] = BLOCK
                    self.b_matrix[rend_i - 1][rend_j + 1] = BLOCK
                    self.b_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if self.grid.south(i, j):
                    self.b_matrix[rend_i + 1][rend_j] = BLOCK
                    self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i + 1][rend_j + 1] = BLOCK
                if  j == 0 and self.grid.west(i, j):
                    self.b_matrix[rend_i][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK

    def draw(self, wall_colour: str, ft_colour: str) -> None:
        GREEN = "\033[0;32m"
        RED = "\033[0;31m"
        BLUE = "\033[0;34m"
        BOLD_YELLOW = "\033[1;33m"
        BG_RED = "\033[41m"  # Background color
        RESET = "\033[0m"
        START = "\033[0;102m"
        END = "\033[0;104m"
        PATH = "\033[0;105m"
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
        center_i = (self.grid.height * 2 + 1) // 2
        center_j = (self.grid.width * 2 + 1) // 2
        if self.grid.width % 2 == 0:
            center_j -= 1
        if self.grid.height % 2 == 0:
            center_i -= 1
        for i in range(self.grid.height * 2 + 1):
            for j in range(self.grid.width * 2 + 1):
                char = self.b_matrix[i][j] * 2
                for coord in self.path:
                    if i == self.start[0] * 2 + 1 and j == self.start[1] * 2 + 1:
                        char = START + char + RESET + wall_colour
                    elif i == self.end[0] * 2 + 1 and j == self.end[1] * 2 + 1:
                        char = END + char + RESET + wall_colour
                    elif i == (coord[0] * 2) + 1 and j == (coord[1] * 2) + 1:
                        char = PATH + char + RESET + wall_colour
                if i >= center_i - 5 and i <= center_i + 5 and j >= center_j - 7 and j <= center_j + 8:
                    if p42[i - (center_i - 5)][j - (center_j - 7)]:
                        print(ft_colour, end='')
                    else:
                        print(wall_colour, end='')

                print(char, end='')
            print()
        print(RESET, end='')

