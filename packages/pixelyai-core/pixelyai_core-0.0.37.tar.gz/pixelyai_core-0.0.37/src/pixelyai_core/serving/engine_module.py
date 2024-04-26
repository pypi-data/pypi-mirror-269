import gradio as gr

from agentx import ServeEngine
import logging
from typing import List, Optional
import transformers

logging.basicConfig(
    level=logging.INFO
)


class AgentXServer(ServeEngine):
    tokenizer: transformers.PreTrainedTokenizerBase | None = None

    def create_gradio_pixely_ai(self):
        with gr.Blocks(theme=gr.themes.Soft()) as block:
            gr.Markdown("# <h3> <center>Powered by [AgentX](https://github.com/erfanzar/AgentX) </center> </h3>")

            with gr.Row():
                with gr.Column():
                    prompt = gr.Textbox(
                        show_label=True,
                        placeholder="Message Box",
                        container=True,
                        label="Message Box"
                    )
                    system = gr.Textbox(
                        show_label=True,
                        placeholder="System",
                        container=True,
                        value="",
                        label="System"
                    )
                    response = gr.Markdown(
                        show_label=True,
                        label="Response"
                    )
                    submit = gr.Button(variant="primary")
            with gr.Row():
                with gr.Accordion("Advanced Options", open=False):
                    max_new_tokens = gr.Slider(
                        value=self.sample_config.max_new_tokens,
                        maximum=10000,
                        minimum=1,
                        label="Max New Tokens",
                        step=1
                    )

            inputs = [
                prompt,
                system,
                max_new_tokens,
            ]
            _ = prompt.submit(
                fn=self.process_pixely_request,
                inputs=inputs,
                outputs=[prompt, response]
            )
            _ = submit.click(
                fn=self.process_pixely_request,
                inputs=inputs,
                outputs=[prompt, response]
            )

            block.queue()
        return block

    def process_pixely_request(
            self,
            prompt: str,
            system: str,
            max_new_tokens: int,
    ):
        conversation = []

        if system is not None and system != "":
            conversation.append({"role": "system", "content": system})
        conversation.append({"role": "user", "content": prompt})
        if self.prompt_template is None:
            prompt = self.tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            prompt = self.prompt_template.render(conversation)
        response = ""
        for char in self.process(
                prompt=prompt,
                max_new_tokens=max_new_tokens,
                max_sequence_length=max_new_tokens
        ):
            response += char
            yield "", response

    def build(
            self,
    ):
        with gr.Blocks(
                theme=gr.themes.Soft(
                    primary_hue=gr.themes.colors.orange,
                    secondary_hue=gr.themes.colors.orange,
                ),
                title="AgentX inference"
        ) as block:
            with gr.Tab("Pixely Serve"):
                self.create_gradio_pixely_ai()
            with gr.Tab("Pixely Chat"):
                self.chat_interface_components()
        return block
