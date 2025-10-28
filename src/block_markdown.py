def markdown_to_blocks(markdown):
    md = markdown.replace("\r\n", "\n").replace("\r", "\n")
    blocks = md.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)

    return filtered_blocks

