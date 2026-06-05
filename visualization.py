from maze_gen import Cell, Grid

BLOCK = "\u2588"
SPACE = " "


class visualizer:
    def __init__(self,
                 grid: Grid,
                 path: list[tuple[int, int]] = []
                 ) -> None:
        self.grid = grid
        self.path = []
        self.start: tuple[int, int] = grid.start
        self.end: tuple[int, int] = grid.end
        self.ground_maker()

    def ground_maker(self) -> None:
        self.b_matrix: list[list[str]] = []
        for i in range(self.grid.height * 2 + 1):
            temp_arr: list[str] = []
            for j in range(self.grid.width * 2 + 1):
                temp_arr.append(" ")
            self.b_matrix.append(temp_arr)

    def input(self,
              matrix: list[list[Cell]] = [],
              render: bool = False
              ) -> None:
        if render:
            self.grid.change_grid(matrix)
            self.ground_maker()
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
                if j == 0 and self.grid.west(i, j):
                    self.b_matrix[rend_i][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i - 1][rend_j - 1] = BLOCK
                    self.b_matrix[rend_i + 1][rend_j - 1] = BLOCK

    def add_path(self, path) -> None:
        true_path: list[tuple[int, int]] = []
        for i in range(len(path) - 1):
            true_path.append((path[i][0] * 2 + 1, path[i][1] * 2 + 1))
            if path[i][0] < path[i + 1][0]:
                true_path.append((path[i + 1][0] * 2, path[i][1] * 2 + 1))
            elif path[i][0] > path[i + 1][0]:
                true_path.append((path[i][0] * 2, path[i][1] * 2 + 1))
            elif path[i][1] < path[i + 1][1]:
                true_path.append((path[i][0] * 2 + 1, path[i + 1][1] * 2))
            else:
                true_path.append((path[i][0] * 2 + 1, path[i][1] * 2))
        self.path = true_path

    def draw(self,
             colours_set: tuple[str, ...],
             ft_flag: bool = False,
             path_flag: bool = False
             ) -> None:

        WALL: str = colours_set[0]
        FT: str = colours_set[1]
        START: str = colours_set[2]
        END: str = colours_set[3]
        PATH: str = colours_set[4]

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
        print(WALL, end='')
        center_i = (self.grid.height * 2 + 1) // 2
        center_j = (self.grid.width * 2 + 1) // 2
        if self.grid.width % 2 == 0:
            center_j -= 1
        if self.grid.height % 2 == 0:
            center_i -= 1
        for i in range(self.grid.height * 2 + 1):
            for j in range(self.grid.width * 2 + 1):
                char = self.b_matrix[i][j] * 2
                if not self.path:

                    if (i == self.start[0] * 2 + 1
                            and j == self.start[1] * 2 + 1):
                        char = START + char + RESET + WALL
                    elif i == self.end[0] * 2 + 1 and j == self.end[1] * 2 + 1:
                        char = END + char + RESET + WALL
                else:
                    for coord in self.path:
                        if (i == self.start[0] * 2 + 1
                                and j == self.start[1] * 2 + 1):
                            char = START + char + RESET + WALL
                        elif i == self.end[0] * 2 + 1 and j == self.end[1] * 2 + 1:
                            char = END + char + RESET + WALL
                        elif path_flag and i == coord[0] and j == coord[1]:
                            char = PATH + char + RESET + WALL
                if (ft_flag
                    and i >= center_i - 5 and i <= center_i + 5
                        and j >= center_j - 7 and j <= center_j + 8):
                    if p42[i - (center_i - 5)][j - (center_j - 7)]:
                        print(FT, end='')
                    else:
                        print(WALL, end='')
                print(char, end='')
            print()
        print(RESET, end='')
