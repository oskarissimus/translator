import logging
import polib
from openai import OpenAI

import logging
from translator.translate_service import TranslateService

from translator.logger import format_log

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)


if __name__ == "__main__":
    input_file = "/home/oskar/git/translator/futurecoder_English.po"
    output_file = "/home/oskar/git/translator/futurecoder_Polish.po"

    po = polib.pofile(input_file)
    client = OpenAI()
    total_entries = len(po)
    translate_service = TranslateService(client, total_entries)
    for index, entry in enumerate(po):
        logging.info(format_log(entry.msgstr, "INPUT"))
        translated = translate_service.translate(entry.msgstr, index)
        entry.msgstr = translated
        logging.info(format_log(entry.msgstr, "OUTPUT"))
        po.save(output_file)
