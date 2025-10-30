import os
from markdown_to_html_node import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = "", ""

    with open(from_path, 'r', encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()
    
    inner_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Content }}", inner_html).replace("{{ Title }}", title)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)
    
def extract_title(markdown):
    md_lines = markdown.splitlines()
    title = ""

    for line in md_lines:
        if line.lstrip().startswith("# "):
            title = line.strip("# ").strip()
            break

    if title != "":
        return title
    else:
        raise Exception("Title not found")