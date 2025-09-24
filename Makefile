.PHONY run rename lint format

run:
	poetry run python src/main.py

rename:
	poetry run python src/main.py --rename-pdf

lint: 
	poetry run ruff check . 

format: 
	poetry run ruff format .