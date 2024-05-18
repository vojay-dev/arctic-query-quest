all:
	@echo "see README.md"

.venv:
	poetry install

.PHONY: run
run:
	poetry run streamlit run arctic_query_quest/main.py

.PHONY: test
test:
	poetry run python -m pytest tests/ -v

.PHONY: ruff
ruff:
	poetry run ruff check --fix
