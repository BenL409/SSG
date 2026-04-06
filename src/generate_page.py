import os
import pathlib
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    raise Exception("markdown does not contain a title")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    node = markdown_to_html_node(markdown)
    content = node.to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Content }}", content).replace("{{ Title }}", title).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, dest_path, basepath)
        elif os.path.isfile(full_path):
            dest_path = pathlib.Path(dest_path).with_suffix(".html")
            generate_page(full_path, template_path, dest_path, basepath)