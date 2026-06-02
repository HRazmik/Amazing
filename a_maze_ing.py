from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid
from dfs import dfs_path
if __name__ == "__main__":
    try:
        config = load_config(sys.argv[1])

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
    matrixxx = Grid(config.height, config.width)
    matrixxx.add_pattern()
    matrixxx.generate()
    path = dfs_path(matrixxx, config.entry, config.exit)
    print(path)
    output = visualizer(matrixxx, config.entry, config.exit, path)
    output.input()
    output.draw("\033[;92m", "\033[36m")