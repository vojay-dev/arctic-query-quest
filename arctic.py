import json
from functools import wraps
from time import sleep
import logging

from langchain_community.llms.replicate import Replicate
from pydantic import BaseModel

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You're are a friendly SQL expert and mentor, here to teach SQL to beginners and advanced users. Your explanations
and questions should be clear and concise, and you should provide helpful examples to illustrate your points.
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
            top_k: int = 50,
            top_p: float = 1.0,
            temperature: float = 0.85,
            max_new_tokens: int = 3072,
            presence_penalty: float = 1.15,
            frequency_penalty: float = 0.2
    ):
        self.llm = Replicate(
            model="snowflake/snowflake-arctic-instruct",
            model_kwargs={
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "max_new_tokens": max_new_tokens,
                "stop_sequences": STOP_SEQUENCE,
                "prompt_template": PROMPT_TEMPLATE,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty
            }
        )

    @retry(max_retries=8)
    def invoke(self, prompt: str) -> ArcticQuiz:
        chunks = []
        for chunk in self.llm.stream(prompt):
            chunks.append(chunk)

        output = "".join(chunks)
        return ArcticQuiz.parse_obj(json.loads(output))
