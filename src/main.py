import sys
import argparse
from copy_static import copy_static
from generate_content import generate_pages_recursive, extract_template_indents
from htmlnode import leading_spaces

# Configuration
dest_path = "docs"
static_path = "static"
content_path = "content"
template_path = "template.html"

# Indent settings
template_indents = extract_template_indents(template_path)

def main(basepath="/", verbose=False):
    if verbose:
        print(f"Base path: {basepath}")
        print(f"template indents\n\tspaces per indent: {template_indents[0]}\n\tbase content indents: {template_indents[1]}\n\tLeading spaces: \"{leading_spaces(template_indents)}\"\n\tnum of leading spaces: {len(leading_spaces(template_indents))}")
    copy_static(static_path, dest_path, verbose=verbose)
    generate_pages_recursive(content_path, template_path, dest_path, base_path=basepath, indents=template_indents, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Static site generator",
                                    description="Generates a static website from content, static, and template files.",
                                    epilog="Example usage: python src/main.py /base/path -v")
    parser.add_argument("basepath", help="base path for the website")
    parser.add_argument("-v", "--verbose", action="store_true", help="print verbose output")
    args = parser.parse_args()

    main(basepath=args.basepath, verbose=args.verbose)
