from textnode import TextNode, TextType
from copystatic import copy_files_recursive
import os
import shutil
import sys
from generate_page import generate_pages_recursive


def main():
    if sys.argv[1:]:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()