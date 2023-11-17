from openai.types.chat import ChatCompletion
import logging

from translator.models import Message


def log_response_tokens(response: ChatCompletion) -> None:
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens
    logging.info(f"{input_tokens=}, {output_tokens=}, {total_tokens=}")


def log_messages_tokens(messages: list[Message]) -> None:
    for message in messages:
        logging.info(f"{message.role=}, {message.token_count=}")


def format_log(input, log_type):
    space_padded_log_type = f" {log_type} "
    formatted_log = f"{space_padded_log_type.center(90, '=')}\n{input}\n{'=' * 90}\n\n"
    return formatted_log
