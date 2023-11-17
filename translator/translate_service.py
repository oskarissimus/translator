from decimal import Decimal
from openai import OpenAI
from translator.const import PERSONALITY
from translator.enums import ModelName
from translator.logger import log_messages_tokens, log_response_tokens
from translator.models import Message, get_messages_dicts
from translator.pricing import calculate_response_cost
from translator.util import get_latest_messages, sum_tokens


class TranslateService:
    def __init__(self, client: OpenAI):
        self.client = client
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

    def translate(self, text: str) -> str:
        self.messages.append(Message(content=text, role="user"))
        latest_messages = get_latest_messages(self.messages)
        response = self.client.chat.completions.create(
            model=self.model, messages=get_messages_dicts(latest_messages)
        )
        input_tokens = response.usage.prompt_tokens
        self.messages[-1].token_count = input_tokens - sum_tokens(latest_messages)

        message = response.choices[0].message
        self.messages.append(
            Message(
                content=message.content,
                role=message.role,
                token_count=response.usage.completion_tokens,
            )
        )
        translated = response.choices[0].message.content
        calculate_response_cost(response, self.model)
        log_response_tokens(response)
        log_messages_tokens(self.messages)

        return translated

    def check_system_message_token_count(self) -> int:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[Message(content=PERSONALITY, role="system").model_dump()],
        )
        return response.usage.prompt_tokens
