from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    md = markdown.replace("\r\n", "\n").replace("\r", "\n")
    blocks = md.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(block):
    if not block:
        return BlockType.PARAGRAPH
    
    lines = block.split("\n")
    if lines[0].startswith("#"):
        count = 0
        for char in lines[0]:
            if char == "#":
                count += 1
            elif char == " " and count <= 6 and lines[0][count + 1:]:
                return BlockType.HEADING
            else: 
                return BlockType.PARAGRAPH
    elif block.strip().startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
