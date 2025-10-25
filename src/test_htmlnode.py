import unittest

from htmlnode import HTMLNode, LeafNode


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
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_nonstandard_tag(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_plain_text(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError)

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertRaises(ValueError)

    def test_leaf_to_html_nonstring_value(self):
        node = LeafNode("p", 8)
        self.assertEqual(node.to_html(), "<p>8</p>")
    

if __name__ == "__main__":
    unittest.main()