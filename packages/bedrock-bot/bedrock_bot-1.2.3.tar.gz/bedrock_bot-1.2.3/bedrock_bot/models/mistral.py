import logging

from rich.console import Console

from .base_model import _BedrockModel

logger = logging.getLogger()

console = Console()


class MistralLarge(_BedrockModel):
    name = "Mistral-Large"
    model_params = {
        "max_tokens": 200,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50,
    }

    def __init__(self, boto_config=None):
        super().__init__(
            model_id="mistral.mistral-large-2402-v1:0", boto_config=boto_config
        )

    def _format_messages(self):
        formatted_messages = ["<s>[INST]"]
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            formatted_message = f"{role}: {content}"
            formatted_messages.append(formatted_message)
        formatted_messages.append("[/INST]")
        return "\n".join(formatted_messages)

    def _create_invoke_body(self) -> dict:
        prompt = self._format_messages()
        body = {"prompt": prompt}
        return body

    def _handle_response(self, body) -> str:
        response_message = body["outputs"][0]

        return response_message["text"]
