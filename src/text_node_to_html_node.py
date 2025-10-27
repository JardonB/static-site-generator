from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(node):
    if not isinstance(node, TextNode):
        raise ValueError("text_node_to_html_node(node): node must be a text node")
    
    if node.text_type not in TextType:
        raise ValueError("invalid text type")
    
    if node.text_type == TextType.TEXT:
        return LeafNode(None, node.text)
    
    if node.text_type == TextType.BOLD:
        return LeafNode("b", node.text)
    
    if node.text_type == TextType.ITALIC:
        return LeafNode("i", node.text)
    
    if node.text_type == TextType.CODE:
        return LeafNode("code", node.text)
    
    if node.text_type == TextType.LINK:
        return LeafNode("a", node.text, {"href": node.url})
    
    if node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})