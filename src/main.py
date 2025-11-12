import sys
from copy_static import copy_static
from generate_content import generate_pages_recursive, extract_template_indents
from htmlnode import leading_spaces

dest_path = "docs"
static_path = "static"
content_path = "content"
template_path = "template.html" 
base_path = "/"
template_indents = extract_template_indents(template_path)
verbose = False

if len(sys.argv) >= 2:
    base_path = sys.argv[1]
    if "--verbose" in sys.argv:
        verbose = True

def main():
    if verbose:
        print(f"template indents\n\tspaces per indent: {template_indents[0]}\n\tbase content indents: {template_indents[1]}\n\tLeading spaces: \"{leading_spaces(template_indents)}\"\n\tnum of leading spaces: {len(leading_spaces(template_indents))}")
    copy_static(static_path, dest_path, verbose=verbose)
    generate_pages_recursive(content_path, template_path, dest_path, base_path, template_indents, verbose=verbose)


if __name__ == "__main__":
    main()
