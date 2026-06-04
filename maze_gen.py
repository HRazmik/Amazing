from random import randint, choice


class Cell:
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
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self. height = height
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
                row.append(Cell( ))
            self.cells.append(row)

    def output(self) -> None:
        fd = open("output_maze.txt", "w+t")
        for line in self.cells:
            hex_line: str = ""
            for cell in line:
                hex_line += f"{cell.walls:X}"
            hex_line += "\n"
            fd.write(hex_line)

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

    def add_pattern(self, flag: bool = False) -> None:
        pattern_ft :list[list[int]]= [
                    [0x1, 0xb, 0xf, 0xf, 0x1, 0x1, 0x1],
                    [0x1, 0xc, 0x7, 0xd, 0x5, 0x7, 0x1],
                    [0x1, 0x1, 0x1, 0xb, 0x1, 0x1, 0x1],
                    [0x7, 0x3, 0x1, 0xa, 0x1, 0xd, 0x7],
                    [0xf, 0xe, 0x1, 0xe, 0x1, 0x1, 0x1]
                ]
        pi = 0
        for i in range(self.center_i - 2, self.center_i + 3):
            pj = 0
            for j in range(self.center_j - 3, self.center_j + 4):
                if pattern_ft[pi][pj] == 0x1:
                    self.cells[i][j].visit()
                elif flag and pattern_ft[pi][pj] != 0x1:
                    self.cells[i][j].walls = pattern_ft[pi][pj]
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

    def wall_destroyer(self,
                       rt:tuple[int, int],
                       ct:tuple[int, int]) -> None:
        atempt = 0
        count = 1
        if self.height * self.width >= 350:
            count = self.height * self.width // 200
        for _ in range(count):
            row = randint(rt[0], rt[1] - 1)
            col = randint(ct[0], ct[1] - 1)
            while len(self.get_neib(row, col)) == 0:
                row = randint(rt[0], rt[1] - 1)
                col = randint(ct[0], ct[1] - 1)
                atempt += 1
            if atempt == 10:
                break
            current = self.cells[row][col]
            if atempt == 10:
                break
            ni, nj = choice(self.get_neib(row, col))
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

    def split_and_sample(self):
        self.set_beck()
        self.add_pattern(False)
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
                self.wall_destroyer((r0, r1), (c0, c1))


    def generate(self,
                 start: tuple[int, int],
                 perfect_flag: bool = True) -> None:
        if self.height > 6 and self.width > 8:
            self.add_pattern(True)
        stack: list[tuple[int, int]] = []
        ci, cj = start
        stack.append((ci, cj))
        while(len(stack) != 0):
            current: Cell = self.cells[ci][cj]
            current.visit()
            try:
                ni, nj = choice(self.get_neib(ci, cj))
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
            except IndexError:
                ci, cj = stack.pop()

        if not perfect_flag:
            self.split_and_sample()
        
