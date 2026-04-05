from textnode import TextNode, TextType
from extractor import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text):
    text_node = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_link(text_node)
    return text_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        for alt_text, url in matches:
            sections = original_text.split(f"![{alt_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        for link_text, url in matches:
            sections = original_text.split(f"[{link_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes