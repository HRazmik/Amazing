from random import randint, choice


class Cell:
    def __init__(self, dev_mode: int = 0xf):
        self.walls = dev_mode #fully closed, (no)
        self.visited = False

    def visit(self) -> None:
        self.visited = True

    def remove_wall(self, direction: int) -> None:
        self.walls &= ~direction
    
    def add_wall(self, direction: int) -> None:
        self.walls |= direction


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self. height = height
        self.cells: list[list[Cell]] = []
        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                row.append(Cell( ))
            self.cells.append(row)

    def get(self, x: int, y: int) -> Cell | None:
        if x >= 0 and y >= 0 and y < self.width and x < self.height:
            return self.cells[x][y]
        
        else:
            return None

    def change_grid(self, matrix: list[list[int]]) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j].walls = matrix[i][j]

    def north(self, i: int, j: int) -> bool:
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x1)

    def east(self, i: int, j: int) -> bool:
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x2)

    def south(self, i: int, j: int) -> bool:
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x4)

    def west(self, i: int, j: int) -> bool:
        value = self.get(i, j)
        if value is None:
            return False
        else:
            return bool(value.walls & 0x8)

    def add_pattern(self) -> None:
        ft_i = 0
        ft_j = 0
        pattern_ft :list[list[bool]]= [
                    [True, False, False, False, True, True, True],
                    [True, False, False, False, False, False, True],
                    [True, True, True, False, True, True, True],
                    [False, False, True, False, True, False, False],
                    [False, False, True, False, True, True, True]
                ]
        center_i = self.height // 2 
        center_j = self.width // 2
        if self.height % 2 == 0:
            center_i -= 1
        if self.width % 2 == 0:
            center_j -= 1
        pi = 0
        for i in range(center_i - 2, center_i + 3):
            pj = 0
            for j in range(center_j - 3, center_j + 4):
                if pattern_ft[pi][pj] is True:
                    self.cells[i][j].visit()
                pj += 1
            pi += 1

    def get_neighbour(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbour = []
        cell = self.cells[i][j]
        if i > 0 and not (cell.walls & 0x1):
            neighbour.append((i - 1, j))
        if j < self.width - 1 and not (cell.walls & 0x2):
            neighbour.append((i, j + 1))
        if i < self.height - 1 and not (cell.walls & 0x4):
            neighbour.append((i + 1, j))
        if j > 0 and not (cell.walls & 0x8):
            neighbour.append((i, j - 1))
        return neighbour
 
    def get_neib(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbour: list[tuple[int, int]] = []
        cell: Cell = self.cells[i][j]
        if i > 0 and (cell.walls & 0x1) and not self.cells[i - 1][j].visited:
            neighbour.append((i - 1, j))
        if j < self.width - 1 and (cell.walls & 0x2) and not self.cells[i][j + 1].visited:
            neighbour.append((i, j + 1))
        if i < self.height - 1 and (cell.walls & 0x4) and not self.cells[i + 1][j].visited:
            neighbour.append((i + 1, j))
        if j > 0 and (cell.walls & 0x8) and not self.cells[i][j - 1].visited:
            neighbour.append((i, j - 1))
        return neighbour

    def set_beck(self) -> None:
        for line in self.cells:
            for cell in line:
                cell.visited = False

    def generate(self, start: tuple[int, int] = (0, 0)) -> None:
        stack: list[tuple[int, int]] = []
        s_i, s_j = start
        
        def recursion(i: int, j: int) -> bool:
            current: Cell = self.cells[i][j]
            current.visit()
            try:
                ni, nj = choice(self.get_neib(i, j))
                if ni < i:
                    current.remove_wall(0x1)
                    self.cells[ni][nj].remove_wall(0x4)
                elif nj < j:
                    current.remove_wall(0x8)
                    self.cells[ni][nj].remove_wall(0x2)
                elif ni > i:
                    current.remove_wall(0x4)
                    self.cells[ni][nj].remove_wall(0x1)
                else:
                    current.remove_wall(0x2)
                    self.cells[ni][nj].remove_wall(0x8)
                stack.append((ni, nj))
            except IndexError:
                if len(stack) == 0:
                    return True
                ni, nj = stack.pop()
            if len(stack) != 0:
                recursion(ni, nj)
            return False
        
        
        recursion(s_i, s_j)
