from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []

    for block in blocks:
        node_list.append(block_to_html_node(block, block_to_block_type(block)))
    
    return ParentNode("div", node_list)

def block_to_html_node(block, block_type):
    if block_type == BlockType.CODE:
        return block_to_code(block)
    elif block_type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    elif block_type == BlockType.HEADING:
        return block_to_heading(block)
    elif block_type == BlockType.QUOTE:
        return block_to_quote(block)
    elif block_type == BlockType.ORDERED_LIST:
        return block_to_ol(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return block_to_ul(block)
    
def block_to_code(block):
    lines = block.splitlines()
    inner = "\n".join(lines[1:-1])
    if not inner.endswith("\n"): inner += "\n"
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, inner)])])

def block_to_paragraph(block):
    lines = block.splitlines()
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))

def block_to_heading(block):
    i = 1
    while block[i] == "#":
        i += 1
    return ParentNode(f"h{i}", text_to_children(block[i+1:]))

def block_to_quote(block):
    line_list = block.splitlines()
    stripped_lines = []
    for line in line_list:
        if line.startswith("> "):
            stripped_lines.append(line[2:])
        elif line.startswith(">"):
            stripped_lines.append(line[1:])
        else:
            stripped_lines.append(line)
    return ParentNode("blockquote", text_to_children("\n".join(stripped_lines)))

def block_to_ol(block):
    node_list = [ParentNode("li", text_to_children(line[3:])) for line in block.split("\n")]
    return ParentNode("ol", node_list)
    
def block_to_ul(block):
    node_list = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
    return ParentNode("ul", node_list)

def text_to_children(text):
    text_node_list = text_to_textnodes(text)
    node_list = []
    for text_node in text_node_list:
        node_list.append(text_node_to_html_node(text_node))

    return node_list