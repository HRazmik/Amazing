from random import randint, choice
from typing import Generator
import time


class Cell:
    """Class representing a single cell in the maze grid."""
    def __init__(self, dev_mode: int = 0xf):
        self.walls = dev_mode
        self.visited = False

    def visit(self) -> None:
        self.visited = True

    def remove_wall(self, direction: int) -> None:
        self.walls &= ~direction

    def add_wall(self, direction: int) -> None:
        self.walls |= direction


class Grid:
    """Class representing the maze grid and its operations."""
    def __init__(self,
                 width: int,
                 height: int,
                 start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        self.width: int = width
        self.height: int = height
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end
        self.cells: list[list[Cell]] = []
        self.center_i = self.height // 2
        self.center_j = self.width // 2
        if self.height % 2 == 0:
            self.center_i -= 1
        if self.width % 2 == 0:
            self.center_j -= 1
        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                row.append(Cell())
            self.cells.append(row)

    def pattern(self) -> bool:
        """ checks if the 42 pattern can be added to the grid

        Returns:
            bool: returns True if the 42 pattern can be added to the grid, otherwise False
        """
        self.pattern_state = False
        if self.width > 8 and self.height > 8:
            self.pattern_state = True
        return self.pattern_state

    def get(self, i: int, j: int) -> Cell | None:
        """ returns the cell by the coordinates if they are correct, otherwise None

        Args:
            i (int): line of the necessary cell
            j (int): column of the necessary cell

        Returns:
            Cell | None: returns the cell if the coordinates are correct, otherwise None
        """
        if i >= 0 and j >= 0 and j < self.width and i < self.height:
            return self.cells[i][j]
        else:
            return None

    def change_grid(self, matrix: list[list[Cell]]) -> None:
        """can be used to change the grid by the new one

        Args:
            matrix (list[list[Cell]]): new grid to change to
        """
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j].walls = matrix[i][j].walls

    def north(self, i: int, j: int) -> bool:
        """chacks if there is a wall in the north direction of the cell with coordinates (i, j)

        Args:
            i (int): coordinates of the cell in the line
            j (int): coordinates of the cell in the column

        Returns:
            bool: returns True if there is a wall in the north direction of the cell with coordinates (i, j), otherwise False
        """
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x1)

    def east(self, i: int, j: int) -> bool:
        """chacks if there is a wall in the east direction of the cell with coordinates (i, j)

        Args:
            i (int): coordinates of the cell in the line
            j (int): coordinates of the cell in the column

        Returns:
            bool: returns True if there is a wall in the east direction of the cell with coordinates (i, j), otherwise False
        """
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x2)

    def south(self, i: int, j: int) -> bool:
        """chacks if there is a wall in the south direction of the cell with coordinates (i, j)

        Args:
            i (int): coordinates of the cell in the line
            j (int): coordinates of the cell in the column

        Returns:
            bool: returns True if there is a wall in the south direction of the cell with coordinates (i, j), otherwise False
        """
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x4)

    def west(self, i: int, j: int) -> bool:
        """chacks if there is a wall in the west direction of the cell with coordinates (i, j)

        Args:
            i (int): coordinates of the cell in the line
            j (int): coordinates of the cell in the column

        Returns:
            bool: returns True if there is a wall in the west direction of the cell with coordinates (i, j), otherwise False
        """
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x8)

    def add_pattern(self, flag: bool = False) -> bool:
        """ adds the 42 pattern in the center of the maze, if flag is True, it also
        adds walls to the cells that are not part of the pattern but are in the 7x5 area around the center

        Args:
            flag (bool, optional): breakes the nacessary walls surounding 42 pattern, if flag is True. Defaults to False.

        Returns:
            bool: returns False if the entry or exit is trapped inside the 42 pattern, otherwise True
        """
        pattern_ft: list[list[int]] = [
                    [0x1, 0xb, 0xf, 0xf, 0x1, 0x1, 0x1],
                    [0x1, 0xc, 0x7, 0xd, 0x5, 0x7, 0x1],
                    [0x1, 0x1, 0x1, 0xb, 0x1, 0x1, 0x1],
                    [0xd, 0x3, 0x1, 0xa, 0x1, 0xd, 0x7],
                    [0xf, 0xe, 0x1, 0xe, 0x1, 0x1, 0x1]
                ]
        pi = 0
        for i in range(self.center_i - 2, self.center_i + 3):
            pj = 0
            for j in range(self.center_j - 3, self.center_j + 4):
                if pattern_ft[pi][pj] == 0x1 and (i, j) == self.start:
                    print(" *** ERROR *** ")
                    print("entry is trapped inside the 42 pattern")
                    print("change the entry coordinates inside config.txt")
                    return False
                elif pattern_ft[pi][pj] == 0x1 and (i, j) == self.end:
                    print(" *** ERROR *** ")
                    print("exit is trapped inside the 42 pattern")
                    print("change the exit coordinates inside config.txt")
                    return False
                if pattern_ft[pi][pj] == 0x1:
                    self.cells[i][j].visit()
                elif flag and pattern_ft[pi][pj] != 0x1:
                    self.cells[i][j].walls = pattern_ft[pi][pj]
                pj += 1
            pi += 1
        return True

    def get_neighbour(self, i: int, j: int) -> list[tuple[int, int]]:
        """Returns a list of neighboring cell coordinates that are accessible (i.e., not blocked by walls) and have not been visited.

        Args:
            i (int): The row index of the current cell.
            j (int): The column index of the current cell.

        Returns:
            list[tuple[int, int]]: A list of tuples, where each tuple contains the coordinates (row, column) of a neighboring cell that can be visited next.
        """
        neighbour: list[tuple[int, int]] = []
        cell: Cell = self.cells[i][j]
        if i > 0 and (cell.walls & 0x1) and not self.cells[i - 1][j].visited:
            neighbour.append((i - 1, j))
        if (j < self.width - 1 and (cell.walls & 0x2)
                and not self.cells[i][j + 1].visited):
            neighbour.append((i, j + 1))
        if (i < self.height - 1 and (cell.walls & 0x4)
                and not self.cells[i + 1][j].visited):
            neighbour.append((i + 1, j))
        if j > 0 and (cell.walls & 0x8) and not self.cells[i][j - 1].visited:
            neighbour.append((i, j - 1))
        return neighbour

    def set_beck(self) -> None:
        """Resets the visited status of all cells in the grid to False, effectively "setting back" the grid to an unvisited state.
        """
        for line in self.cells:
            for cell in line:
                cell.visited = False

    def wall_destroyer(self,
                       rt: tuple[int, int],
                       ct: tuple[int, int],
                       count: int) -> None:
        """Randomly destroys walls between cells in a specified rectangular region of the grid to create additional paths.

        Args:
            rt (tuple[int, int]): A tuple representing the range of row indices (start, end) for the rectangular region where walls will be destroyed.
            ct (tuple[int, int]): A tuple representing the range of column indices (start, end) for the rectangular region where walls will be destroyed.
        """
        atempt: int = 0
        for _ in range(count):
            row: int = randint(rt[0], rt[1] - 1)
            col: int = randint(ct[0], ct[1] - 1)
            while len(self.get_neighbour(row, col)) == 0:
                row = randint(rt[0], rt[1] - 1)
                col = randint(ct[0], ct[1] - 1)
                atempt += 1
                if atempt == 8:
                    break
            if atempt == 8:
                continue
            current: Cell = self.cells[row][col]
            ni, nj = choice(self.get_neighbour(row, col))

            if ni < row:
                current.remove_wall(0x1)
                self.cells[ni][nj].remove_wall(0x4)
            elif nj < col:
                current.remove_wall(0x8)
                self.cells[ni][nj].remove_wall(0x2)
            elif ni > row:
                current.remove_wall(0x4)
                self.cells[ni][nj].remove_wall(0x1)
            else:
                current.remove_wall(0x2)
                self.cells[ni][nj].remove_wall(0x8)

    def seek_and_destroy(self,
                         render_flag: bool = False,

                         ) -> Generator[list[list[Cell]], None, None]:
        """ makes the maze imperfect by randomly destroying walls between 
        cells in different regions of the grid, while optionally yielding
        the state of the grid after each destruction for rendering purposes.

        Args:
            render_flag (bool, optional): if render_flag is True, and yields
            the final state of the grid after all wall destructions if render_flag
            is False. Defaults to False.

        Yields:
            Generator[list[list[Cell]], None, None]: yields the state of the grid
            (as a list of lists of Cell objects) after each wall destruction .
        """
        self.set_beck()
        if self.pattern_state:
            self.add_pattern(False)
        count: int = self.height * self.width // 100 + 1

        if self.height < 9 and self.width < 9:
            for _ in range(4):
                self.wall_destroyer((0, self.height - 1), (0, self.width - 1), count)
                if render_flag:
                    yield self.cells
            return
        else:
            row_mid_start = self.center_i - 2
            col_mid_start = self.center_j - 3
            row_mid_end = row_mid_start + 5
            col_mid_end = col_mid_start + 7
            row_bands = [
                (0,             row_mid_start),
                (row_mid_start, row_mid_end),
                (row_mid_end,   self.height),
            ]
            col_bands = [
                (0,             col_mid_start),
                (col_mid_start, col_mid_end),
                (col_mid_end,   self.width),
            ]
            for i, (r0, r1) in enumerate(row_bands):
                for j, (c0, c1) in enumerate(col_bands):
                    if i == 1 and j == 1:
                        continue
                    self.wall_destroyer((r0, r1), (c0, c1), count)
                    if render_flag:
                        yield self.cells
        if not render_flag:
            yield self.cells
            return

    def generate(self,
                 render_flag: bool = False
                 ) -> Generator[list[list[Cell]], None, None]:
        """_summary_

        Args:
            render_flag (bool, optional): _description_. Defaults to False.

        Yields:
            Generator[list[list[Cell]], None, None]: _description_
        """
        if self.pattern_state:
            if not self.add_pattern(True):
                exit()
        else:
            print("42 pattern do not fit in")
        stack: list[tuple[int, int]] = []
        ci, cj = self.start
        stack.append((ci, cj))
        while len(stack) != 0:
            current: Cell = self.cells[ci][cj]
            current.visit()
            try:
                ni, nj = choice(self.get_neighbour(ci, cj))
                if ni < ci:
                    current.remove_wall(0x1)
                    self.cells[ni][nj].remove_wall(0x4)
                elif nj < cj:
                    current.remove_wall(0x8)
                    self.cells[ni][nj].remove_wall(0x2)
                elif ni > ci:
                    current.remove_wall(0x4)
                    self.cells[ni][nj].remove_wall(0x1)
                else:
                    current.remove_wall(0x2)
                    self.cells[ni][nj].remove_wall(0x8)
                stack.append((ni, nj))
                ci, cj = ni, nj
                if render_flag:
                    yield self.cells
            except IndexError:
                ci, cj = stack.pop()
        yield self.cells
        return
