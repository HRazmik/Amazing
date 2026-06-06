from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid
from dfs import dfs_path, path_to_str
import os
from output import output

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

colours = [
    ("\033[37m", "\033[33m", "\033[45m", "\033[44m", "\033[42m"),
    ("\033[32m", "\033[36m", "\033[41m", "\033[45m", "\033[43m"),
    ("\033[93m", "\033[92m", "\033[44m", "\033[107m", "\033[101m")
]

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = load_config(sys.argv[1])
    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        sys.exit(1)

    ft_flag: bool = False
    path_flag: bool = False
    render: bool = False
    n: int = 0
    path: list = []
    maze_generated: bool = False

    matrixxx = Grid(config.height, config.width, config.entry, config.exit)
    output_vs = visualizer(matrixxx)

    maze_obj = matrixxx.generate(render, True)
    for cells in maze_obj:
        output_vs.input(cells, render)
        clear_terminal()
        output_vs.draw(colours[n])
    path = dfs_path(matrixxx, config.entry, config.exit)
    output(matrixxx, path_to_str(path))
    maze_generated = True

    status: int = 0
    while status != 6:
        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colours")
        print("4. Turn on/off 42 pattern colour")
        print("5. Re-generate with render animation (BONUS)")
        print("6. Quit")

        try:
            status = int(input("Choice? (1-6): "))
        except ValueError:
            print("Please input a number (1-6)")
            continue

        if status == 1:
            matrixxx = Grid(config.height, config.width, config.entry, config.exit)
            output_vs = visualizer(matrixxx)
            maze_obj = matrixxx.generate(False, True)
            for cells in maze_obj:
                output_vs.input(cells, False)
                clear_terminal()
                output_vs.draw(colours[n])
            path = dfs_path(matrixxx, config.entry, config.exit)
            output(matrixxx, path_to_str(path))

        elif status == 2:
            if not maze_generated:
                print("No maze generated yet")
                continue
            path_flag = not path_flag
            output_vs.add_path(path)  
            clear_terminal()
            output_vs.draw(colours[n], ft_flag, path_flag)

        elif status == 3:
            n = (n + 1) % 3
            clear_terminal()
            output_vs.draw(colours[n], ft_flag, path_flag)

        elif status == 4:
            ft_flag = not ft_flag
            clear_terminal()
            output_vs.draw(colours[n], ft_flag, path_flag)

        elif status == 5:
            matrixxx = Grid(config.height, config.width, config.entry, config.exit)
            output_vs = visualizer(matrixxx)
            maze_obj = matrixxx.generate(True, True)
            for cells in maze_obj:
                output_vs.input(cells, True)
                clear_terminal()
                output_vs.draw(colours[n])
            path = dfs_path(matrixxx, config.entry, config.exit)
            output(matrixxx, path_to_str(path))

        elif status == 6:
            break

        else:
            print("Please input a number (1-6)")

if __name__ == "__main__":
    main()