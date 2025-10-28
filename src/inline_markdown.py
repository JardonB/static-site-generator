import re
from textnode import TextNode, TextType

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            node_list.append(node)
        else:
            parts = node.text.split(delimiter)

            if len(parts) == 1:
                node_list.append(node)
                continue
            elif len(parts) % 2 == 0:
                raise Exception(f"for node: {node} unmatched delimiter: {delimiter}")

            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                elif i % 2 == 0:
                    node_list.append(TextNode(parts[i], TextType.TEXT))
                else:
                    node_list.append(TextNode(parts[i], text_type))
    return node_list

def split_nodes_images(old_nodes):
    node_list = []
    for node in old_nodes:
        node_text = node.text
        image_list = extract_markdown_images(node.text)
        if len(image_list) == 0:
            node_list.append(node)
            continue

        for image in range(len(image_list)):
            alt_text = image_list[image][0]
            url = image_list[image][1]
            pre_text = node_text.split("![" + alt_text, 1)[0] #text before alt_text

            if pre_text != "":
                node_list.append(TextNode(pre_text, TextType.TEXT))
            node_list.append(TextNode(alt_text, TextType.IMAGE, url))

            node_text = node_text.split(url + ")", 1)[1]
        if node_text != "":
            node_list.append(TextNode(node_text, TextType.TEXT))
    return node_list

def split_nodes_links(old_nodes):
    node_list = []
    for node in old_nodes:
        node_text = node.text
        link_list = extract_markdown_links(node.text)
        if len(link_list) == 0:
            node_list.append(node)
            continue

        for link in range(len(link_list)):
            alt_text = link_list[link][0]
            url = link_list[link][1]
            pre_text = node_text.split("[" + alt_text, 1)[0] #text before alt_text

            if pre_text != "":
                node_list.append(TextNode(pre_text, TextType.TEXT))
            node_list.append(TextNode(alt_text, TextType.LINK, url))

            node_text = node_text.split(url + ")", 1)[1]
        if node_text != "":
            node_list.append(TextNode(node_text, TextType.TEXT))
    return node_list

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(((?:[^()\s]|(?:\([^()]*\)))*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(((?:[^()\s]|(?:\([^()]*\)))*)\)"
    matches = re.findall(pattern, text)
    return matches