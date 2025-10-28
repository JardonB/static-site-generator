import unittest

from textnode import TextNode, TextType
from extract_markdown import extract_markdown_links, extract_markdown_images
from text_to_textnodes import text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a different bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an italic text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://boots.dev")
        node2 = TextNode("This is a link text node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_not_eq_when_None(self):
        node = TextNode("This is a link text node", TextType.LINK)
        node2 = TextNode("This is a link text node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

class TestExtractFromMD(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected_result = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a second ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected_result = [("image", "https://i.imgur.com/zjjcJKZ.png"),("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to [boot.dev](https://boot.dev)"
        )
        expected_result = [("boot.dev", "https://boot.dev")]
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is a link to [boot.dev](https://boot.dev) and a second link to [boot.dev](https://boot.dev)"
        )
        expected_result = [("boot.dev", "https://boot.dev"),("boot.dev", "https://boot.dev")]
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_link_from_img(self):
        matches = extract_markdown_links(
            "![image](url)"
        )
        expected_result = []
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_img_from_link(self):
        matches = extract_markdown_images(
            "[anchor](url)"
        )
        expected_result = []
        self.assertListEqual(expected_result, matches)
    
    def test_extract_markdown_link_with_quote(self):
        matches = extract_markdown_links(
            '[anchor](https://quotes.com/quote="true")'
        )
        expected_result = [("anchor", 'https://quotes.com/quote="true"')]
        self.assertListEqual(expected_result, matches)
    
    def test_extract_markdown_img_with_quote(self):
        matches = extract_markdown_images(
            '![image](https://quotes.com/quote="true")'
        )
        expected_result = [("image", 'https://quotes.com/quote="true"')]
        self.assertListEqual(expected_result, matches)

    def test_extract_markdown_empty_parts(self):
        self.assertListEqual([("", "u")], extract_markdown_images("![](u)"))
        self.assertListEqual([("alt", "")], extract_markdown_images("![alt]()"))
        self.assertListEqual([("", "u")], extract_markdown_links("[](u)"))
        self.assertListEqual([("text", "")], extract_markdown_links("[text]()"))

    def test_extract_markdown_broken_syntax_no_match(self):
        self.assertListEqual([], extract_markdown_links("[text](missing"))
        self.assertListEqual([], extract_markdown_images("![alt]missing"))
    
    def test_extract_markdown_no_separator(self):
        self.assertListEqual([("a","u"), ("b","v")], extract_markdown_images("![a](u)![b](v)"))

    def test_parentheses_in_url(self):
        self.assertListEqual([("a","https://ex.com/i_(1).png")], extract_markdown_images("![a](https://ex.com/i_(1).png)"))
        self.assertListEqual([("x","https://ex.com/path_(v2)")], extract_markdown_links("[x](https://ex.com/path_(v2))"))

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_plain_text(self):
        text = "This is plain text"
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is plain text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_only_whitespace(self):
        text = "   "
        new_nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("   ", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()