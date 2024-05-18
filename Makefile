all:
	@echo "see README.md"

.venv:
	poetry install

.PHONY: run
run:
	streamlit run main.py

.PHONY: test
test:
	python -m unittest -v

.PHONY: ruff
ruff:
	ruff check --fix
