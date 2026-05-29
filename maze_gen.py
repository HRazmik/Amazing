import random


class Cell:
    def __init__(self, dev_mode: int = 0x0):
        self.walls = dev_mode #fully closed, (no)

    # def has_wall(self, direction: int) -> bool:
    #     return bool(self.walls & direction)

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
                row.append(Cell())
            self.cells.append(row)

    def get(self, x: int, y: int) -> Cell | None:
        if x >= 0 and y >= 0 and y < self.width and x < self.height:
            return self.cells[x][y]
        else:
            return None

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


# === grdon@ sksec ===
    def generate(self) -> None:

        flag = True
        for i in range(self.height):
            for j in range(self.width):
                if i == 0:
                    self.cells[i][j].add_wall(0x1)
                elif i == self.height - 1:
                    self.cells[i][j].add_wall(0x4)
                if j == 0:
                    self.cells[i][j].add_wall(0x8)

                elif j == self.width - 1:
                    self.cells[i][j].add_wall(0x2)
    def add_pattern(self) -> None:
        ft_i = 0
        ft_j = 0
        pattern_ft :list[list[int]]= [
                    [0xf, 0x8, 0x0, 0x2, 0xf, 0xf, 0xf],
                    [0xf, 0xc, 0x4, 0x0, 0x5, 0x7, 0xf],
                    [0xf, 0xf, 0xf, 0xa, 0xf, 0xf, 0xf],
                    [0x1, 0x3, 0xf, 0xa, 0xf, 0xd, 0x5],
                    [0x0, 0x2, 0xf, 0xa, 0xf, 0xf, 0xf]
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
                self.cells[i][j].add_wall(pattern_ft[pi][pj])
                pj += 1
            pi += 1

                