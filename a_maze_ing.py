from config_parsing import load_config
import sys
from visualization import visualizer
from maze_gen import Grid

if __name__ == "__main__":
    try:
        config = load_config(sys.argv[1])

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
    matrixxx = Grid(config.height, config.width)
    matrixxx.generate()
    matrixxx.add_pattern()

    output = visualizer(matrixxx, config.entry, config.exit)
    output.input()
    output.draw("\033[1;92m", "\033[;36m")
