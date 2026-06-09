from maze_gen import Grid


def output(file_name: str, maze: Grid, path: str) -> None:
    """ 
    Output the maze structure and solution path to a text file.
    Args:
        maze (Grid): Maze grid containing cells and wall structure.
        path (str): solution path from start to end, represented as a string.
    """
    hex_lines: str = ""
    for line in maze.cells:
        hex_line: str = ""
        for cell in line:
            hex_line += f"{cell.walls:X}"
        hex_lines += hex_line + '\n'
        try:
            with open(file_name, "w+t") as fd:
                fd.write(hex_lines)
                fd.write(f"\n{maze.start}\n")
                fd.write(f"{maze.end}\n")
                fd.write(path + "\n")
        except OSError:
            print("Error with output file")
        except UnicodeEncodeError:
            print("Error with output file")
