from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid
from random import seed
from dfs import dfs_path, path_to_str
import os
from output import output

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

colours = [
    ("\033[37m", "\033[33m", "\033[45m", "\033[44m", "\033[42m"),
    ("\033[32m", "\033[36m", "\033[41m", "\033[45m", "\033[43m"),
    ("\033[93m", "\033[92m", "\033[44m", "\033[107m", "\033[101m")]

def main() -> None:
    if len(sys.argv) > 2:
        print("ERROR: Too many arguments")
        exit(0)
    try:
        config = load_config(sys.argv[1])
    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
    status: int = 1
    ft_flag: bool = False
    path_flag: bool = False
    seed(config.seed)
    matrixxx = Grid(config.height, config.width, config.entry, config.exit)
    output_vs = visualizer(matrixxx)
    render = False
    n = 0
    while status != 6:
        if status == 2:
            if path_flag:
                path_flag = False
            else:
                path_flag = True
            output_vs.add_path(path)
        elif status == 3:
            n = (n + 1) % 3
        elif status == 4:
            if ft_flag:
                ft_flag = False
            else:
                ft_flag = True
        elif status == 5:
            if render:
                render = False
            else:
                render = True
                status = 1
        if status == 1:
            maze_obj = matrixxx.generate(render, True)
            for cells in maze_obj:
                output_vs.input(cells, render)
                clear_terminal()
                output_vs.draw(colours[n])
            path = dfs_path(matrixxx, config.entry, config.exit)
            output(matrixxx, path_to_str(path))
        else:
            clear_terminal()
            output(matrixxx, path_to_str(path))
            output_vs.draw(colours[n], ft_flag, path_flag)
        if status == 0:
            print("Please input number (1-5)")
        else:
            print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colours")
        print("4. Turn on/off 42 pattern colour")
        print("5. Re-generate a new maze and renderanimation(BONUS)")
        print("6. Quit")
        try:
            status = int(input("Choice? (1-5): "))
        except ValueError:
            status = 0
    

if __name__ == "__main__":
    main()