from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

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
        