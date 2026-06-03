from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid
from dfs import dfs_path

colours = ("\033[37m", "\033[36m", "\033[41m", "\033[42m", "\033[43m", )
colours_2 = ("\033[32m", "\033[36m", "\033[41m", "\033[42m", "\033[43m", )
if __name__ == "__main__":
    try:
        config = load_config(sys.argv[1])

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
    matrixxx = Grid(config.height, config.width)
    matrixxx.add_pattern()
    matrixxx.generate(config.entry, False)
    # path = dfs_path(matrixxx, config.entry, config.exit)
    # # print(path)
    # output = visualizer(matrixxx, config.entry, config.exit, path)
    # output.input()
    # output.draw(colours)


    matrixxx.split_and_sample()
    matrixxx.output()
    path = dfs_path(matrixxx, config.entry, config.exit)
    # print(path)
    output_2 = visualizer(matrixxx, config.entry, config.exit, path)
    output_2.input()
    output_2.draw(colours_2)