import sys
from copy_static import copy_static
from generate_content import generate_pages_recursive

dest_path = "docs"
static_path = "static"
content_path = "content"
template_path = "template.html" 
base_path = "/"

if sys.argv[0]:
    base_path = sys.argv[0]

def main():
    copy_static(static_path, dest_path)
    generate_pages_recursive(content_path, template_path, dest_path, base_path)


if __name__ == "__main__":
    main()
