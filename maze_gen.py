import random


class Cell:
    def __init__(self):
        self.walls = 0xF #fully closed

    def has_wall(self, direction: int) -> bool:
        return bool(self.walls & direction)
    
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

    def get(self, x: int, y: int) -> Cell:
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return self.cells[y][x]
        else:
            return None
        
 


