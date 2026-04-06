from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os
import shutil
from generate_page import generate_pages_recursive


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    
main()