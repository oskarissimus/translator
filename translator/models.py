from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str
    role: str
    token_count: int = Field(default=0, exclude=True)


def get_messages_dicts(messages: list[Message]) -> list[dict[str, str]]:
    return [message.model_dump() for message in messages]
