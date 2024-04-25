from typing import Optional
from jinja2 import Environment, BaseLoader
import os

PROMPT = open(f"{os.path.dirname(__file__)}/prompt.jinja2", "r").read().strip()


class ChatAgent:
    def __init__(
            self,
            **kwargs
    ):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def render(
            prompt: str,
            conversation: Optional[list[list[str]]] = None
    ) -> str:
        template = Environment(loader=BaseLoader()).from_string(PROMPT)
        return template.render(
            conversation=conversation,
            prompt=prompt
        )
