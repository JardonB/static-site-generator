import unittest

from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes import split_nodes_images, split_nodes_links


class TestSplitNodeDelimiter(unittest.TestCase):
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

class TestSplitNodeImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode("This node does not contain an image", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual([node], new_nodes)

    def test_starts_with_image(self):
        node = TextNode("![img](src) is an image", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("img", TextType.IMAGE, "src"),
                TextNode(" is an image", TextType.TEXT)
            ]
        )

class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode("This node does not contain a link", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_starts_with_link(self):
        node = TextNode("[link](src) is a link", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "src"),
                TextNode(" is a link", TextType.TEXT)
            ]
        )

if __name__ == "__main__":
    unittest.main()