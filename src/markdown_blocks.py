from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"
    
def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for char in blocks:
        cleaned = char.strip()
        if cleaned == "":
            continue
        filtered_blocks.append(cleaned)
    return filtered_blocks     
    
def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    elif block.startswith("1. "):
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
            counter += 1
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html(block))
        elif type == BlockType.HEADING:
            children.append(heading_to_html(block))
        elif type == BlockType.CODE:
            children.append(code_to_html(block))
        elif type == BlockType.QUOTE:
            children.append(quote_to_html(block))
        elif type == BlockType.ULIST:
            children.append(ulist_to_html(block))
        elif type == BlockType.OLIST:
            children.append(olist_to_html(block))
        else:
            raise ValueError("invalid block type")
    return ParentNode("div", children)

def paragraph_to_html(block):
    lines = block.split("\n")
    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("p", children)

def heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html(block):
    text = block[4:-3]
    node = TextNode(text, TextType.TEXT)
    code = text_node_to_html_node(node)
    children = ParentNode("code", [code])
    return ParentNode("pre", [children])

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html(block):
    lines = block.split("\n")
    node_list = []
    for line in lines:
        children = text_to_children(line[2:])
        node_list.append(ParentNode("li", children))
    return ParentNode("ul", node_list)

def olist_to_html(block):
    lines = block.split("\n")
    node_list = []
    for line in lines:
        text = line.split(". ", 1)
        children = text_to_children(text[1])
        node_list.append(ParentNode("li", children))
    return ParentNode("ol", node_list)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children 
        