import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
# Heading



This is a paragraph.



- item one
- item two
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "- item one\n- item two",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph with no separations."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no separations."])

    def test_markdown_to_blocks_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only(self):
        md = "\n\n   \n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_strips_whitespace(self):
        md = "   # Heading with leading/trailing spaces   \n\n   Paragraph text   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading/trailing spaces",
                "Paragraph text",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH
        )

    def test_code(self):
        block = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_multiline(self):
        block = "```\nline one\nline two\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_unclosed_is_paragraph(self):
        block = "```\nprint('hello world')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = ">This is a quote\n>with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_space(self):
        block = "> This is a quote\n> with a space after >"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_missing_marker_is_paragraph(self):
        block = ">This is a quote\nbut this line isn't"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_is_paragraph(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        block = "2. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number_is_paragraph(self):
        block = "1. item one\n3. item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a heading

## This is an h2 heading with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is an h2 heading with <b>bold</b> text</h2></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> spanning multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item **two**
- item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. item one
2. item two
3. item _three_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item one</li><li>item two</li><li>item <i>three</i></li></ol></div>",
        )

    def test_all_block_types_together(self):
        md = """
# Heading

This is a paragraph with `code` in it

> a quote

- one
- two

1. first
2. second

```
raw code
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <code>code</code> in it</p>"
            "<blockquote>a quote</blockquote>"
            "<ul><li>one</li><li>two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<pre><code>raw code\n</code></pre>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
