import unittest
from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
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

class TestBlockToBlockType(unittest.TestCase):
    def test_normal_paragraph(self):
        block = "This is a\nparagraph"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_abnormal_paragraph(self):
        block = "> This is also\n- A paragraph"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_heading(self):
        block = "# This is a\n# heading"
        block_type = block_to_block_type(block)
        expected_result = BlockType.HEADING
        self.assertEqual(block_type, expected_result)

    def test_max_hashes(self):
        block = "###### Is a heading"
        block_type = block_to_block_type(block)
        expected_result = BlockType.HEADING
        self.assertEqual(block_type, expected_result)

    def test_no_content_head(self):
        block = "## "
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_if_newline_breaks_count(self):
        block = "## \n##\n##"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_too_many_hashes(self):
        block = "####### Not a heading"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_no_space_head(self):
        block = "#No space"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_code(self):
        block = "```for code in code_block:\n\tprint(code)```"
        block_type = block_to_block_type(block)
        expected_result = BlockType.CODE
        self.assertEqual(block_type, expected_result)

    def test_quote(self):
        block = "> This is a\n>quote"
        block_type = block_to_block_type(block)
        expected_result = BlockType.QUOTE
        self.assertEqual(block_type, expected_result)

    def test_quote_missing_line(self):
        block = "> This is\nnot a\n> quote"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        block_type = block_to_block_type(block)
        expected_result = BlockType.UNORDERED_LIST
        self.assertEqual(block_type, expected_result)

    def test_unordered_list_missing_line(self):
        block = "- one\n- two\n- three\n four"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        block_type = block_to_block_type(block)
        expected_result = BlockType.ORDERED_LIST
        self.assertEqual(block_type, expected_result)

    def test_ordered_list_not_ordered(self):
        block = "1. one\n2. two\n3. three\n5. five"
        block_type = block_to_block_type(block)
        expected_result = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected_result)
