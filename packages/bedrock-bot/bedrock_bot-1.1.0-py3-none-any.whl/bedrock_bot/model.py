import json
import logging
from enum import Enum

import boto3
from botocore.config import Config
from rich.console import Console

logger = logging.getLogger()

console = Console()


class ConversationRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value


class _BedrockModel:
    """
    Base class for all models. Usage:
    Add a message to the conversation and invoke the model with `model.invoke(message)`.

    Creating new implementations of this base model:
    - Define extra params to inject to the invoke call on self._model_params
    - Provide a model_id to `super().__init__()`
    - If your model needs a different body than the default, overwrite `self._create_invoke_body()`
    """

    _model_params = {}
    name = "Base Model"

    def __init__(
        self,
        model_id: str,
        boto_config=None,
    ):
        self._model_id = model_id
        if not boto_config:
            boto_config = Config()
        self._bedrock = boto3.client("bedrock-runtime", config=boto_config)
        self.messages = []

    def reset(self):
        self.messages = []

    def append_message(self, role: ConversationRole, message: str):
        self.messages.append({"role": role.value, "content": message})

    def invoke(self, message: str):
        self.append_message(ConversationRole.USER, message)

        logger.info(f"Sending current messages to AI: {self.messages}")
        response = self._invoke()
        self.append_message(ConversationRole.ASSISTANT, response)
        return response

    def _create_invoke_body(self) -> dict:
        raise NotImplementedError

    def _handle_response(self, body) -> str:
        raise NotImplementedError

    def _invoke(self):
        body = self._create_invoke_body() | self._model_params

        with console.status("[bold green]Waiting for response..."):
            response = self._bedrock.invoke_model(
                modelId=self._model_id, body=json.dumps(body)
            )
            body = json.loads(response["body"].read())

            output = self._handle_response(body)

        return output


class _Claude3(_BedrockModel):
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
        self._model_params = {
            "max_tokens": 2000,
            "temperature": 1,
            "top_k": 250,
            "top_p": 0.999,
            "stop_sequences": ["\n\nHuman:"],
            "anthropic_version": "bedrock-2023-05-31",
        }

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


class MistralLarge(_BedrockModel):
    name = "Mistral-Large"

    def __init__(self, boto_config=None):
        self._model_params = {
            "max_tokens": 200,
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 50,
        }
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
