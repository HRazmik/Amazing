install:
	poetry install
run:
	poetry run python3 a_maze_ing.py config.txt
debug:
	python3 -m pdb a_maze_ing.py config.txt
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .vscode
	rm -rf .idea
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
lint-strict:
	flake8 .
	mypy . --strict
