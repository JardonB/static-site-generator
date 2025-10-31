import os, logging
from markdown_to_html_node import markdown_to_html_node

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s: %(message)s",
    filename="logs/log.log",
    filemode="w"
)

def generate_page(from_path, template_path, dest_path, base_path):
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = "", ""

    with open(from_path, 'r', encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()
    
    inner_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Content }}", inner_html)    #Fill content with inner_html
    html = html.replace("{{ Title }}", title)               #Replace title with extracted title
    html = html.replace('href="/', f'href="{base_path}')    #Replace href path with base_path
    html = html.replace('src="/', f'src="{base_path}')      #Replace src path with base_path

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    contents = os.listdir(dir_path_content)
    for item in contents:
        file_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(file_path):
            if file_path.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, (f"{item.split(".")[0]}.html"))
                generate_page(file_path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, base_path)
    
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