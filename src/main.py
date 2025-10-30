from copy_static import copy_static
from generate_content import generate_page

public_path = "./public/"
static_path = "./static/"

def main():
    copy_static(static_path, public_path)
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
