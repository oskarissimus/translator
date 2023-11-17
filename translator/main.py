from decimal import Decimal
import logging
import polib
from openai import OpenAI

import logging
from translator.translate_service import TranslateService

from translator.util import format_log

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)


if __name__ == "__main__":
    client = OpenAI()
    translate_service = TranslateService(client)
    input_file = "/home/oskar/git/translator/futurecoder_English.po"
    output_file = "/home/oskar/git/translator/futurecoder_Polish.po"

    po = polib.pofile(input_file)
    for entry in po:
        logging.info(format_log(entry.msgstr, "INPUT"))
        translated = translate_service.translate(entry.msgstr)
        entry.msgstr = translated
        logging.info(format_log(entry.msgstr, "OUTPUT"))
        po.save(output_file)
