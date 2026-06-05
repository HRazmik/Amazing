from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid
from dfs import dfs_path
import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

# Call the function whenever you need to clean the screen
colours = ("\033[37m", "\033[36m", "\033[41m", "\033[42m", "\033[43m", )
colours_2 = ("\033[32m", "\033[36m", "\033[41m", "\033[45m", "\033[43m", )
if __name__ == "__main__":
    try:
        config = load_config(sys.argv[1])

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
    matrixxx = Grid(config.height, config.width, config.entry, config.exit)

    # path = dfs_path(matrixxx, config.entry, config.exit)
    output_2 = visualizer(matrixxx, [])
    render = False
    vzgo = matrixxx.generate(render)
    for cells in vzgo:
        output_2.input(cells, render)
        clear_terminal()
        output_2.draw(colours_2, True)
    matrixxx.output()