import unittest

from page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_from_multiline(self):
        md = """
Some intro text

# The Real Title

Some more content
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_extract_title_ignores_h2(self):
        md = """
## Not an h1

# This is the h1
"""
        self.assertEqual(extract_title(md), "This is the h1")

    def test_extract_title_no_h1_raises(self):
        md = """
## Just an h2

Some paragraph text
"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_space_after_hash_not_matched(self):
        md = "#NoSpaceHere\n\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")


if __name__ == "__main__":
    unittest.main()
