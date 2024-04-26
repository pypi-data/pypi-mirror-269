import gradio_client as gc
import functools
from typing import List
from .prompt_templates import ChatAgent, RAGAgent

END_OF_MESSAGE_TURN_HUMAN = "<|END_OF_MESSAGE_TURN_HUMAN|>"
END_OF_MESSAGE = "<|END_OF_MESSAGE|>"


def format_chat_for_ai_client(user: List[str], assistance: List[str]):
    history = ""
    for c1, c2 in zip(user, assistance):
        history += f"{c1}{END_OF_MESSAGE_TURN_HUMAN}{c2}{END_OF_MESSAGE}"
    return history


class PixelClient:
    def __init__(
            self,
            url_client: str,
    ):
        self.client = gc.Client(
            url_client,
            verbose=False,
            max_workers=128
        )

    def __call__(
            self,
            prompt: str,
            conversation_history: List[dict] = None,
            contexts: List[str] = None,
            debug: bool = False,
            max_new_tokens: int = 2048
    ) -> str:
        """

        :param prompt:string
        :param conversation_history:[{"user": ..., "assistance": ..., ...}]
        :param contexts: List of Contexts [str]
        :param debug: Bool
        :param max_new_tokens: int
        :return: response
        """

        conversation = None

        if contexts is not None:
            if conversation_history is not None:
                conversation = []
                for user, assistant in zip(
                        [f["user"] for f in conversation_history],
                        [f["assistance"] for f in conversation_history]
                ):
                    conversation.append(
                        [user, assistant]
                    )
            prompt = RAGAgent.render(
                prompt=prompt,
                conversation=conversation,
                contexts=contexts
            )
        else:
            if conversation_history is not None:
                conversation = []
                for user, assistant in zip(
                        [f["user"] for f in conversation_history],
                        [f["assistance"] for f in conversation_history]
                ):
                    conversation.append(
                        [user, assistant]
                    )

            prompt = ChatAgent.render(
                prompt=prompt,
                conversation=conversation
            )

        return self.client.predict(
            prompt,
            "",
            max_new_tokens,
            api_name="/process_pixely_request"
        )[-1]
