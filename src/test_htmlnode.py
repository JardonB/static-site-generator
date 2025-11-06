import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from textnode import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty_node(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", inline=True)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_nonstandard_tag(self):
        node = LeafNode("span", "Hello, world!", inline=True)
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>\n')

    def test_leaf_to_html_plain_text(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError)

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>\n")
    
    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(),"<p></p>\n")

    def test_leaf_to_html_nonstring_value(self):
        node = LeafNode("p", 8, inline=True)
        self.assertEqual(node.to_html(), "<p>8</p>")

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", inline=True),
                LeafNode(None, "Normal text", inline=True),
                LeafNode("i", "italic text", inline=True),
                LeafNode(None, "Normal text", inline=True),
            ],
            inline=True
        )
        expected_result = "<p>\n<b>Bold text</b>Normal text<i>italic text</i>Normal text\n</p>\n"
        self.assertEqual(node.to_html(), expected_result)

    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "i",
                    [
                        LeafNode(None, "italic text1", inline=True),
                        LeafNode(None, "italic text2", inline=True),
                    ]
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = "<p>\n<b>Bold text</b>\nNormal text<i>\nitalic text1italic text2\n</i>\nNormal text\n</p>\n"
        self.assertEqual(node.to_html(), expected_result)

    def test_deep_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    ParentNode(
                        "i",
                        LeafNode(
                            "a",
                            "google.com",
                            {
                                "href": "google.com"
                            }, inline=True
                        ), inline=True
                    ), inline=True
                )
            ], inline=True
        )
        expected_result = '<p>\n<b><i><a href="google.com">google.com</a></i></b>\n</p>\n'
        self.assertEqual(node.to_html(), expected_result)

    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text")
            ]
        )
        with self.assertRaises(ValueError):
            html = node.to_html()
    
    def test_no_children(self):
        node = ParentNode(
            "b",
            None
        )
        with self.assertRaises(ValueError):
            html = node.to_html()

    def test_untagged_children(self):
        node = ParentNode(
            "b",
            [
                LeafNode(None, "Bold text")
            ]
        )
        self.assertEqual(node.to_html(), "<b>\nBold text\n</b>\n")

    def test_mixed_tagged_children(self):
        node = ParentNode(
            "b",
            [
                LeafNode(None, "Bold text", inline=True),
                LeafNode("i", "Bold and italic text", inline=True)
            ], 
            inline=True
        )
        self.assertEqual(node.to_html(), "<b>Bold text<i>Bold and italic text</i></b>\n")

    def test_parent_to_html_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", inline=True),
                LeafNode(None, "Normal text", inline=True),
                ParentNode(
                    "i",
                    [
                        LeafNode(None, "italic text1", inline=True),
                        LeafNode(None, "italic text2", inline=True),
                    ],
                    inline=True
                ),
                LeafNode(None, "Normal text", inline=True),
            ],
            props={
                "style": "text-align:right",
            },
            inline=True
        )
        expected_result = '<p style="text-align:right">\n<b>Bold text</b>Normal text<i>italic text1italic text2</i>\nNormal text\n</p>\n'
        self.assertEqual(node.to_html(), expected_result)

    def test_single_child_direct(self):
        node = ParentNode(
            "b",
            LeafNode(None, "Bold text")
        )
        self.assertEqual(node.to_html(), "<b>\nBold text\n</b>\n")

    def test_whitespace_preservation(self):
        node = ParentNode(
            "b",
            [
                LeafNode("i", " "),
                LeafNode("i", " text ")
            ]
        )
        self.assertEqual(node.to_html(), "<b>\n<i> </i>\n<i> text </i>\n</b>\n")

    def test_multiple_props(self):
        node = ParentNode(
            "b",
            LeafNode(None, "Bold text"),
            {
                "one": "1",
                "two": "2"
            }, 
            inline=True
        )
        self.assertEqual(node.to_html(), '<b one="1" two="2">Bold text</b>\n')
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode(None, "This is a text node")
        self.assertEqual(html_node.to_html(), expected_result.to_html()) # type: ignore

    def test_nontextnode_node(self):
        node = "This is not a text node"
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)

    def test_invalid_texttype(self):
        with self.assertRaises(ValueError):
            node = TextNode("invalid text type", None)
      
    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode("b", "bold text")
        self.assertEqual(html_node.to_html()+"\n", expected_result.to_html()) # type: ignore
    
    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode("i", "italic text")
        self.assertEqual(html_node.to_html()+"\n", expected_result.to_html()) # type: ignore
    
    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode("code", "code text")
        self.assertEqual(html_node.to_html()+"\n", expected_result.to_html()) # type: ignore
    
    def test_link(self):
        node = TextNode("anchor text", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode("a", "anchor text", {"href": "google.com"})
        self.assertEqual(html_node.to_html()+"\n", expected_result.to_html()) # type: ignore
    
    def test_image(self):
        node = TextNode("an image", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        expected_result = LeafNode("img", "", {"src":"image.jpg", "alt":"an image"})
        self.assertEqual(html_node.to_html()+"\n", expected_result.to_html()) # type: ignore

if __name__ == "__main__":
    unittest.main()