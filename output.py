from maze_gen import Grid


def output(maze: Grid, path: str) -> None:
    hex_lines: str = ""
    for line in maze.cells:
        hex_line: str = ""
        for cell in line:
            hex_line += f"{cell.walls:X}"
        hex_lines += hex_line + '\n'
        with open("output_maze.txt", "w+t") as fd:
            fd.write(hex_lines)
            fd.write(f"\n{maze.start}\n")
            fd.write(f"{maze.end}\n")
            fd.write(path + "\n")
