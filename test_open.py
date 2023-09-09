import unittest

from open import generate_options


class GenerateOptionsTestCase(unittest.TestCase):
    def test_when_only_one_match_exists(self):
        options = [x for x in generate_options(['ki'])]
        self.assertListEqual(options, ['kibana'])

    def test_if_no_words_match(self):
        options = [x for x in generate_options(['zzz'])]
        self.assertListEqual(options, [])

    def test_when_options_exist(self):
        options = [x for x in generate_options(['cal'])]
        self.assertEqual(len(options), 11)  # google-calendar & calendar

    def test_when_three_words(self):
        options = [x for x in generate_options(['gh', 'repos', 'rss-mvc'])]
        self.assertEqual(len(options), 4)


if __name__ == '__main__':
    unittest.main()
