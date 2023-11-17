from decimal import Decimal
from openai import OpenAI
from translator.const import PERSONALITY
from translator.enums import ModelName
from translator.logger import (
    log_grand_total_cost,
    log_messages_tokens,
    log_response_tokens,
    log_total_cost,
)
from translator.models import Message, get_messages_dicts
from translator.pricing import calculate_response_cost
from translator.util import get_latest_messages, sum_tokens
from openai.types.chat import ChatCompletion


def calculate_last_message_token_count(
    input_tokens: int, messages: list[Message]
) -> int:
    return input_tokens - sum_tokens(messages)


class TranslateService:
    def __init__(self, client: OpenAI, total_entries: int) -> None:
        self.client = client
        self.total_entries = total_entries
        self.total_cost = Decimal("0.00")
        self.model = ModelName.GPT_4_1106_PREVIEW
        system_message_token_count = self.check_system_message_token_count()
        self.messages = [
            Message(
                content=PERSONALITY,
                role="system",
                token_count=system_message_token_count,
            )
        ]

    def translate(self, text: str, index: int) -> str:
        self.append_user_message(text)
        response = self.create_chat_completion()
        self.update_last_message_token_count(response)
        self.append_response_message(response)
        self.log_and_calculate_costs(response)
        self.estimate_grand_total_cost(index)

        return response.choices[0].message.content

    def append_user_message(self, text: str) -> None:
        self.messages.append(Message(content=text, role="user"))

    def create_chat_completion(self) -> ChatCompletion:
        latest_messages = get_latest_messages(self.messages)
        return self.client.chat.completions.create(
            model=self.model, messages=get_messages_dicts(latest_messages)
        )

    def update_last_message_token_count(self, response: ChatCompletion) -> None:
        input_tokens = response.usage.prompt_tokens
        latest_messages = get_latest_messages(self.messages)
        last_message_token_count = calculate_last_message_token_count(
            input_tokens, latest_messages
        )
        self.messages[-1].token_count = last_message_token_count

    def append_response_message(self, response: ChatCompletion) -> None:
        message = response.choices[0].message
        self.messages.append(
            Message(
                content=message.content,
                role=message.role,
                token_count=response.usage.completion_tokens,
            )
        )

    def log_and_calculate_costs(self, response: ChatCompletion) -> None:
        cost = calculate_response_cost(response, self.model)
        self.total_cost += cost
        log_total_cost(self.total_cost)
        log_response_tokens(response)
        log_messages_tokens(self.messages)

    def check_system_message_token_count(self) -> int:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[Message(content=PERSONALITY, role="system").model_dump()],
        )
        return response.usage.prompt_tokens

    def estimate_grand_total_cost(self, index: int) -> None:
        cost_per_entry = self.total_cost / (index + 1)
        grand_total_cost = cost_per_entry * self.total_entries
        log_grand_total_cost(grand_total_cost)
