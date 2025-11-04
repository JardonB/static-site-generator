import os, logging
from markdown_to_html_node import markdown_to_html_node

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s: %(message)s",
    filename="logs/log.log",
    filemode="w"
)

def generate_page(from_path, template_path, dest_path, base_path, indents = [0, 0]):
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = "", ""

    with open(from_path, 'r', encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()
    
    inner_html = markdown_to_html_node(markdown, indents).to_html()
    if inner_html.endswith("\n"):
        inner_html = inner_html[:-1]
    title = extract_title(markdown)
    lead_spaces = " " * (indents[0] * indents [1])

    html = template.replace(lead_spaces + "{{ Content }}", inner_html)    #Fill content with inner_html
    html = html.replace("{{ Title }}", title)               #Replace title with extracted title
    html = html.replace('href="/', f'href="{base_path}')    #Replace href path with base_path
    html = html.replace('src="/', f'src="{base_path}')      #Replace src path with base_path

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path, indents = [0, 0]):
    contents = os.listdir(dir_path_content)
    for item in contents:
        file_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(file_path):
            if file_path.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, (f"{item.split(".")[0]}.html"))
                generate_page(file_path, template_path, dest_path, base_path, indents)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, base_path, indents)
    
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
    
def extract_template_indents(template_path): 
    content_line, first_indented_line = "", ""
    indent_spaces = 0 #indent spaces is the number of spaces per indent
    content_depth = 0 #content depth is the number of indents for the content
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()

    for line in template.splitlines():
        if line.startswith(" ") and first_indented_line == "":
            first_indented_line = line #The first line that starts with space will be used to calculate spaces per indent 
        if "{{ Content }}" in line:
            content_line = line        #The line where our content will be inserted
            break
    
    counter = 0
    for i in range(len(first_indented_line)):
        if first_indented_line[i] == " ": counter += 1
        else: break
    indent_spaces = counter
    counter = 0
    for i in range(len(content_line)):
        if content_line[i] == " ": counter += 1
        else: break
    content_depth = counter // indent_spaces

    return [indent_spaces, content_depth]


