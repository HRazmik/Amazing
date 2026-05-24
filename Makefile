install:
	pip install -r requirements.txt
run:
	python a_maze_ing.py
debug:
	#vzgo
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
