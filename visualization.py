from mazegen import Cell, Grid

BLOCK = "\u2588"
SPACE = " "


class visualizer:
    """A class to visualize the maze in the terminal.
    """
    def __init__(self,
                 grid: Grid
                 ) -> None:
        self.grid = grid
        self.path: list[tuple[int, int]] = []
        self.start: tuple[int, int] = grid.start
        self.end: tuple[int, int] = grid.end
        self.ground_maker()

    def ground_maker(self) -> None:
        """Initializes the base visualization matrix (b_matrix) with spaces,
        creating a grid that is twice the size of the maze dimensions plus one
        to accommodate walls and paths.
        This matrix serves as the canvas for rendering the maze structure and
        solution path.
        """
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
        """ Updates the visualization matrix (b_matrix) based on the current
        state of the maze grid.

        If the render flag is set to True, it first updates the grid with the
        provided matrix and then calls ground_maker to reset the visualization
        matrix.
        It iterates through each cell in the maze grid and updates the
        corresponding positions in b_matrix to represent walls using BLOCK
        characters based on the presence of walls in eachdirection
        (north, east, south, west) for each cell.

        Args:
            matrix (list[list[Cell]], optional): matrix of Cells to input in
            visualization matrix. Defaults to [].
            render (bool, optional): _description_. Defaults to False.
        """
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

    def add_path(self, path: list[tuple[int, int]]) -> None:
        """ receives a path represented as a list of coordinates (tuples) and
        converts it into a format suitable for visualization.
        The method iterates through the provided path, which consists of cell
        coordinates in the maze grid, and translates them into corresponding
        coordinates in the visualization matrix (b_matrix).
        For each pair of consecutive coordinates in the path, it calculates
        the intermediate coordinates that represent the path between those
        two points in

        Args:
            path (list[tuple[int, int]]): A list of tuples representing the
            coordinates of the path in the maze grid. Each tuple contains the
            row and column indices of a cell in the maze.
        """
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
        """ Renders the maze visualization in the terminal using the provided
        color settings and flags for additional features.

        Args:
            colours_set (tuple[str, ...]): A tuple containing color codes for
            different elements of the maze visualization. The expected order
            is (WALL, FT, START, END, PATH).
            ft_flag (bool, optional): A flag indicating whether to render the
            "42" pattern in the center of the maze. Defaults to False.
            path_flag (bool, optional): A flag indicating whether to render
            the solution path from the start to the end of the maze. Defaults
            to False.
        """
        WALL: str = colours_set[0]
        FT: str = colours_set[1]
        START: str = colours_set[2]
        END: str = colours_set[3]
        PATH: str = colours_set[4]
        RESET = "\033[0m"
        if self.grid.height < 9 or self.grid.width < 9:
            ft_flag = False
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
                if not path_flag:

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
                        elif (i == self.end[0] * 2 + 1
                              and j == self.end[1] * 2 + 1):
                            char = END + char + RESET + WALL
                        elif i == coord[0] and j == coord[1]:
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
