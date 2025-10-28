import unittest
from block_markdown import (
    markdown_to_blocks,
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(blocks, expected_result)
    
    def test_excessive_newlines(self):
        md = "\n\n\nText\n\n\n"
        blocks = markdown_to_blocks(md)
        expected_result = ["Text"]
        self.assertEqual(blocks, expected_result)

    def test_excessive_newlines_mid(self):
        md = "First\n\n\nSecond"
        blocks = markdown_to_blocks(md)
        expected_result = ["First", "Second"]
        self.assertEqual(blocks, expected_result)

    def test_whitespace_removed(self):
        md = "First     \n\n        Second"
        blocks = markdown_to_blocks(md)
        expected_result = ["First", "Second"]
        self.assertEqual(blocks, expected_result)

    def test_newlines_only(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        expected_result = []
        self.assertEqual(blocks, expected_result)
  
    def test_single_block(self):
        md = "This is a single block"
        blocks = markdown_to_blocks(md)
        expected_result = ["This is a single block"]
        self.assertEqual(blocks, expected_result)

    def test_windows_newlines(self):
        md = "First\r\n\rSecond"
        blocks = markdown_to_blocks(md)
        expected_result = ["First", "Second"]
        self.assertEqual(blocks, expected_result)

    def test_varied_newlines(self):
        md = "First\n\nSecond\n\n\nThird\n\n\n\nFourth"
        blocks = markdown_to_blocks(md)
        expected_result = ["First", "Second", "Third", "Fourth"]
        self.assertEqual(blocks, expected_result)
              
    def test_preserved_indents(self):
        md = "Para 1 line 1\n  indented line 2\n\nNext"
        blocks = markdown_to_blocks(md)
        expected_result = ["Para 1 line 1\n  indented line 2", "Next"]
        self.assertEqual(blocks, expected_result)

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        expected_result = []
        self.assertEqual(blocks, expected_result)