from unittest import TestCase

from src.offish import get_version


class TestVersion(TestCase):
    def test_version(self):
        version = get_version("offish", "twitchtube", "twitchtube")

        self.assertEqual(version, "1.6.6")
