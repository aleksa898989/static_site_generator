import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        block = raw_block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    while block[level] == "#":
        level += 1
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    lines = block.split("\n")
    code_text = "\n".join(lines[1:-1]) + "\n"
    code_leaf = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for i, line in enumerate(block.split("\n")):
        text = line[len(f"{i + 1}. ") :]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
