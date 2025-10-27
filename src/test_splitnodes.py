import unittest

from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNode(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_split_multi(self):
        node = TextNode("This is `text` with multiple `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with multiple ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_split_no_delimiter(self):
        node = TextNode("This is text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([node], new_nodes)
    
    def test_unmatched_delimiter(self):
        node = TextNode("This is text with `an unmatched delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_starts_with_delimiter(self):
        node = TextNode("**This** text starts with a delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This", TextType.BOLD),
            TextNode(" text starts with a delimiter", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_result) 

    def test_split_mixed_type(self):
        nodes = [
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is a text node with an _italicised_ word", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected_result = [
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is a text node with an ", TextType.TEXT),
            TextNode("italicised", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_result)


if __name__ == "__main__":
    unittest.main()