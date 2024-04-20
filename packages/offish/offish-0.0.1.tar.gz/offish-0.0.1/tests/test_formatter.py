from unittest import TestCase

from src.offish.formatter import Formatter, FileFormatter

import logging


class TestFormatter(TestCase):
    def test_formatter(self):
        formatter = Formatter()
        formatter.application = "test_formatter"

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])

        logging.warning("debug")

    def test_file_formatter(self):
        formatter = FileFormatter()
        formatter.application = "test_file_formatter"

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])

        logging.warning("debug2")
