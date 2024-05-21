import json
import logging
import re
from functools import wraps
from time import sleep

from langchain_community.llms.replicate import Replicate
from pydantic import BaseModel

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You're are a friendly SQL expert and mentor, here to teach SQL to beginners and advanced users. Your explanations
and questions are clear and concise, and you provide helpful examples to illustrate your points.
"""

PROMPT_TEMPLATE = f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n<|im_start|>user\n{{prompt}}<|im_end|>\n\n<|im_start|>assistant\n"
STOP_SEQUENCE = "<|im_end|>"


class ArcticQuiz(BaseModel):
    question: str
    answer_1: str
    answer_2: str
    answer_3: str
    correct_answer: int
    explanation: str


def retry(max_retries: int) -> callable:
    def decorator(func) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    logger.error(f"error in {func.__name__}: {e}")
                    if _ < max_retries - 1:
                        logger.warning(f"retrying {func.__name__}...")
                        sleep(1)
                    else:
                        raise e

        return wrapper

    return decorator


class ArcticClient:

    def __init__(
            self,
            top_k: int = 35,
            top_p: float = 1.0,
            temperature: float = 0.7,
            min_new_tokens: int = 0,
            max_new_tokens: int = 7000,
            presence_penalty: float = 0.8,
            frequency_penalty: float = 0.2
    ):
        self.llm = Replicate(
            model="snowflake/snowflake-arctic-instruct",
            model_kwargs={
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "min_new_tokens": min_new_tokens,
                "max_new_tokens": max_new_tokens,
                "stop_sequences": STOP_SEQUENCE,
                "prompt_template": PROMPT_TEMPLATE,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty
            }
        )

    @staticmethod
    def _extract_json(text: str) -> str:
        regex = r"^.*(\{.+\}).*$"
        matches = re.search(regex, text, re.MULTILINE | re.DOTALL)
        if not matches or len(matches.groups()) != 1:
            raise ValueError(f"text contains none or too many JSON objects: {text}")

        return matches.group(1)

    def _parse_output(self, text: str) -> ArcticQuiz:
        json_text = self._extract_json(text)
        return ArcticQuiz.model_validate(json.loads(json_text.lstrip().rstrip()))

    @retry(max_retries=8)
    def invoke(self, prompt: str) -> ArcticQuiz:
        chunks = []
        for chunk in self.llm.stream(prompt):
            chunks.append(chunk)

        output = "".join(chunks)
        return self._parse_output(output)
