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
                print(self.cells[i][j].walls, end=' ')
            print()