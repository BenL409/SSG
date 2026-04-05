import unittest
from markdown_blocks import markdown_to_blocks
    
class TestMarkdownBlock(unittest.TestCase):
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
    
    def test_excessive_lines(self):
        md = """
This is a **bolded** paragraph


This line is after two lines
The next line is here

- Here's a list
- Second item on list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This line is after two lines\nThe next line is here",
                "- Here's a list\n- Second item on list"
            ],
        )