import logging

from rich.console import Console

from .base_model import _BedrockModel

logger = logging.getLogger()

console = Console()


class _Claude3(_BedrockModel):
    model_params = {
        "max_tokens": 2000,
        "temperature": 1,
        "top_k": 250,
        "top_p": 0.999,
        "stop_sequences": ["\n\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31",
    }

    def _create_invoke_body(self) -> dict:
        body = {
            "messages": self.messages,
        }

        return body

    def _handle_response(self, body) -> str:
        response_message = body["content"][0]

        if response_message["type"] != "text":
            raise RuntimeError(
                "Unexpected response type to prompt: " + response_message["type"]
            )

        return response_message["text"]

    def __init__(self, model_id: str, boto_config=None):
        super().__init__(
            model_id=model_id,
            boto_config=boto_config,
        )


class Claude3Sonnet(_Claude3):
    name = "Claude-3-Sonnet"

    def __init__(self, boto_config=None):
        super().__init__(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            boto_config=boto_config,
        )


class Claude3Haiku(_Claude3):
    name = "Claude-3-Haiku"

    def __init__(self, boto_config=None):
        super().__init__(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            boto_config=boto_config,
        )
