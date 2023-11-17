from decimal import Decimal
import logging
from openai import OpenAI
from translator.const import PERSONALITY
from translator.pricing import calculate_cost
from openai.types.chat import ChatCompletion, ChatCompletionMessage
import logging

from pydantic import BaseModel


class Message(BaseModel):
    content: str
    role: str

    @classmethod
    def from_chat_completion_message(cls, message: ChatCompletionMessage):
        return cls(content=message.content, role=message.role)


def create_message(text):
    return Message(content=text, role="user")


class TranslateService:
    def __init__(self, client: OpenAI):
        self.client = client
        self.total_cost = Decimal("0.00")
        self.messages = [
            Message(content=PERSONALITY, role="system"),
        ]
        self.model = "gpt-3.5-turbo-1106"

    def translate(self, text: str) -> str:
        self.messages.append(create_message(text))
        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages
        )
        self.messages.append(
            Message.from_chat_completion_message(response.choices[0].message)
        )
        translated = response.choices[0].message.content
        self.report_tokens(response)
        self.report_cost(response)

        return translated

    def report_cost(self, response: ChatCompletion) -> None:
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = calculate_cost(self.model, input_tokens, output_tokens)
        self.total_cost += cost
        logging.info(f"Cost: {cost}")
        logging.info(f"Total cost: {self.total_cost}")

    def report_tokens(self, response: ChatCompletion) -> None:
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        logging.info(f"Tokens: {input_tokens} input, {output_tokens} output")
