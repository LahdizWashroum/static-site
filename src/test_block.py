import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_nodes
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Ordered item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Regular paragraph."), BlockType.PARAGRAPH)
    def test_block_to_block_type_edge_cases(self):
        self.assertEqual(block_to_block_type("   # Heading with spaces"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code block with spaces```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("   > Quote with spaces"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("   - List item with spaces"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("   1. Ordered item with spaces"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("   Regular paragraph with spaces."), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNodes(unittest.TestCase):
    def test_markdown_to_html_nodes(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
            """

        html_nodes = markdown_to_html_nodes(md)
        self.assertEqual(len(html_nodes), 2)
        self.assertEqual(html_nodes[0][0], BlockType.PARAGRAPH)
        self.assertEqual(html_nodes[1][0], BlockType.PARAGRAPH)
    def test_markdown_to_html_nodes_with_heading(self):
        md = """
            # Heading 1

            This is a paragraph under heading 1.

            ## Heading 2

            This is a paragraph under heading 2.
            """

        html_nodes = markdown_to_html_nodes(md)
        self.assertEqual(len(html_nodes), 4)
        self.assertEqual(html_nodes[0][0], BlockType.HEADING)
        self.assertEqual(html_nodes[1][0], BlockType.PARAGRAPH)
        self.assertEqual(html_nodes[2][0], BlockType.HEADING)
        self.assertEqual(html_nodes[3][0], BlockType.PARAGRAPH)
    def test_markdown_to_html_nodes_with_code_block(self):
        md = """
            ```python
            def hello_world():
                print("Hello, world!")
            ```

            This is a paragraph after the code block.
            """

        html_nodes = markdown_to_html_nodes(md)
        self.assertEqual(len(html_nodes), 2)
        self.assertEqual(html_nodes[0][0], BlockType.CODE)
        self.assertEqual(html_nodes[1][0], BlockType.PARAGRAPH)
    def test_inline_bold_markdown_is_rendered(self):
        md = """This is **bold** text.

![portrait](/portrait.png)

# **Bold heading**

- **Bold list item**

> **Bold quote**"""

        html_nodes = markdown_to_html_nodes(md)

        self.assertEqual(
            [node.to_html() for _, node in html_nodes],
            [
                "<p>This is <b>bold</b> text.</p>",
                '<p><img src="/portrait.png" alt="portrait"></p>',
                "<h1><b>Bold heading</b></h1>",
                "<ul><li><b>Bold list item</b></li></ul>",
                "<blockquote><b>Bold quote</b></blockquote>",
            ],
        )
if __name__ == "__main__":
    unittest.main()