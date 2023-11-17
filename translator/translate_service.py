from decimal import Decimal
import logging
from openai import OpenAI
from translator.const import PERSONALITY
from translator.pricing import calculate_cost
from openai.types.chat import ChatCompletion, ChatCompletionMessage
import logging

from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str
    role: str
    token_count: int = Field(default=0, exclude=True)


def create_message(text):
    return Message(content=text, role="user")


def sum_tokens(messages: list[Message]) -> int:
    return sum([message.token_count for message in messages])


class TranslateService:
    def __init__(self, client: OpenAI):
        self.client = client
        self.total_cost = Decimal("0.00")
        self.messages = [Message(content=PERSONALITY, role="system")]
        self.model = "gpt-3.5-turbo-1106"

    def get_messages_dicts(self) -> list[dict[str, str]]:
        return [message.model_dump() for message in self.messages]

    def translate(self, text: str) -> str:
        self.messages.append(create_message(text))
        response = self.client.chat.completions.create(
            model=self.model, messages=self.get_messages_dicts()
        )
        input_tokens = response.usage.prompt_tokens
        self.messages[-1].token_count = input_tokens - sum_tokens(self.messages)

        message = response.choices[0].message
        self.messages.append(
            Message(
                content=message.content,
                role=message.role,
                token_count=response.usage.completion_tokens,
            )
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

        for message in self.messages:
            logging.info(f"Tokens: {message.token_count} {message.role}")
