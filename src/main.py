import sys

from copystatic import copy_static_to_public
from page import generate_pages_recursive

STATIC_DIR = "static"
PUBLIC_DIR = "docs"
CONTENT_DIR = "content"
TEMPLATE_PATH = "template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public(STATIC_DIR, PUBLIC_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR, basepath)


main()
