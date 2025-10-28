from textnode import TextNode, TextType
from split_nodes import split_nodes_images, split_nodes_links
from split_nodes_delimiter import split_nodes_delimiter

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]

    #split links and images
    node_list = split_nodes_links(node_list)
    node_list = split_nodes_images(node_list)

    #split other text types
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)

    return node_list