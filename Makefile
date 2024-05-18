all:
	@echo "see README.md"

.venv:
	poetry install

.PHONY: run
run:
	streamlit run arctic_query_quest/main.py

.PHONY: test
test:
	python -m unittest -v

.PHONY: ruff
ruff:
	ruff check --fix
