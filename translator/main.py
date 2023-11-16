from decimal import Decimal
import logging
import polib
from openai import OpenAI
from translator.pricing import calculate_cost

import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

client = OpenAI()

total_cost = Decimal("0.00")


def format_log(input, log_type):
    space_padded_log_type = f" {log_type} "
    formatted_log = f"{space_padded_log_type.center(90, '=')}\n{input}\n{'=' * 90}\n\n"
    return formatted_log


def create_messages(text):
    return [
        {
            "role": "system",
            "content": f"You are a helpful assistant that translates texts from python course English to Polish.",
        },
        {"role": "user", "content": text},
    ]


def translate_text(text):
    logging.info(format_log(text, "INPUT"))
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=create_messages(text),
    )
    translated = response.choices[0].message.content
    logging.info(format_log(translated, "OUTPUT"))
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    cost = calculate_cost("gpt-4-1106-preview", input_tokens, output_tokens)
    global total_cost
    total_cost += cost
    logging.info(f"tokens: {input_tokens+output_tokens}")
    logging.info(f"Cost: {cost}")
    logging.info(f"Total cost: {total_cost}")

    return translated


def translate_po_file(input_file, output_file):
    po = polib.pofile(input_file)
    for entry in po:
        translated = translate_text(entry.msgstr)


translate_po_file(
    "/home/oskar/git/translator/futurecoder_English.po",
    "/home/oskar/git/translator/futurecoder_Polish.po",
)
