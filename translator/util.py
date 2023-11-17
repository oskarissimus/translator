from translator.models import Message


def sum_tokens(messages: list[Message]) -> int:
    return sum([message.token_count for message in messages])


def get_latest_messages(messages: list[Message], threshold: int = 1000):
    total_tokens = sum_tokens(messages)
    if total_tokens <= threshold:
        return messages

    messages_copy = messages.copy()

    while sum_tokens(messages_copy) > threshold:
        messages_copy.pop(1)

    return messages_copy
