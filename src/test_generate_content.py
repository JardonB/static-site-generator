import unittest
from generate_content import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Title
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)
  
    def test_extract_title_multiple_h1(self):
        md = """
# Title
# Title 2
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)
     
    def test_extract_title_whitespace(self):
        md = """
  # Title
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)
  
    def test_extract_title_not_first_line(self):
        md = """
Something
something
something
# Title
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)
  
    def test_extract_title_with_following_lines(self):
        md = """
# Title
Something
something
something
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)
  
    def test_extract_title_leading_trailing_whitespace(self):
        md = """
#      Title     
"""
        title = extract_title(md)
        expected_result = "Title"
        self.assertEqual(title, expected_result)

    def test_no_title(self):
        md = """
Not a title
Still not a title
This surely is not a title
"""
        with self.assertRaises(Exception):
            title = extract_title(md)
  