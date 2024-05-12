import json

from langchain_community.llms.replicate import Replicate
from pydantic import BaseModel


class ArcticQuiz(BaseModel):
    question: str
    answer_1: str
    answer_2: str
    answer_3: str
    correct_answer: int
    explanation: str


class ArcticClient:

    def __init__(
            self,
            top_k: int = 50,
            top_p: float = 0.8,
            temperature: float = 0.5,
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
                "stop_sequences": "<|im_end|>",
                "prompt_template": "<|im_start|>system\nYou're a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n",
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty
            }
        )

    def invoke(self, prompt: str) -> ArcticQuiz:
        chunks = []
        for chunk in self.llm.stream(prompt):
            chunks.append(chunk)

        output = "".join(chunks)
        return ArcticQuiz.parse_obj(json.loads(output))
