from enum import StrEnum
from pathlib import Path

from langchain_core.prompts import PromptTemplate

BASE_PATH = 'templates'
MAIN_TEMPLATE = 'prompt.jinja'
DIFFICULTY_PATH = 'difficulty'


class Difficulty(StrEnum):
    EASY = 'easy.jinja'
    MEDIUM = 'medium.jinja'
    HARD = 'hard.jinja'


def get_difficulty_by_name(name: str) -> Difficulty:
    try:
        return Difficulty[name.upper()]
    except KeyError:
        return Difficulty.EASY


class PromptGenerator:

    def __init__(self):
        self.base_template = PromptTemplate.from_file(
            template_file=Path(f"{BASE_PATH}/{MAIN_TEMPLATE}"),
            template_format="jinja2"
        )

    def generate_prompt(
        self,
        model: str,
        difficulty: Difficulty
    ) -> str:
        difficulty_template = PromptTemplate.from_file(
            template_file=Path(f"{BASE_PATH}/{DIFFICULTY_PATH}/{difficulty.value}"),
            template_format="jinja2"
        )

        return self.base_template.format(
            model=model,
            difficulty=difficulty_template.format()
        )
