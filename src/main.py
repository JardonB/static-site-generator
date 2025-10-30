from copy_static import copy_static
from generate_content import generate_pages_recursive

public_path = "./public/"
static_path = "./static/"

def main():
    copy_static(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
