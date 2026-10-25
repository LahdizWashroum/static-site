from enum import Enum
import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_underscore_delimiters_render_as_italic(self):
        nodes = text_to_textnodes("Disney _didn't ruin it_")

        self.assertEqual(
            "".join(text_node_to_html_node(node).to_html() for node in nodes),
            "Disney <i>didn't ruin it</i>",
        )

    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is a *bold* text", TextType.PLAIN),
            TextNode("This is an *italic* text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is an ", TextType.PLAIN),
            TextNode("italic", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_no_plain(self):
        old_nodes = [
            TextNode("This is a *bold* text", TextType.BOLD),
            TextNode("This is an *italic* text", TextType.ITALIC)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a *bold* text", TextType.BOLD),
            TextNode("This is an *italic* text", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_empty(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    def test_extract_markdown_images_no_match(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_no_match(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This is a ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.PLAIN),
            TextNode("This is another ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is another ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_image_no_plain(self):
        old_nodes = [
            TextNode("This is a ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is another ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png")
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
            TextNode("This is a ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is another ![image](https://i.imgur.com/zjjcJKZ.png) text", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_image_empty(self):
        old_nodes = []
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This is a [link](https://example.com) text", TextType.PLAIN),
            TextNode("This is another [link](https://example.com) text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, url="https://example.com"),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is another ", TextType.PLAIN),
            TextNode("link", TextType.LINK, url="https://example.com"),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_link_no_plain(self):
        old_nodes = [
            TextNode("This is a [link](https://example.com) text", TextType.LINK, url="https://example.com"),
            TextNode("This is another [link](https://example.com) text", TextType.LINK, url="https://example.com")
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
            TextNode("This is a [link](https://example.com) text", TextType.LINK, url="https://example.com"),
            TextNode("This is another [link](https://example.com) text", TextType.LINK, url="https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_link_empty(self):
        old_nodes = []
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is a *bold* text", TextType.PLAIN),
            TextNode("This is an *italic* text", TextType.PLAIN)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is an ", TextType.PLAIN),
            TextNode("italic", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_no_plain(self):
        old_nodes = [
            TextNode("This is a *bold* text", TextType.BOLD),
            TextNode("This is an *italic* text", TextType.ITALIC)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a *bold* text", TextType.BOLD),
            TextNode("This is an *italic* text", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    def test_split_nodes_delimiter_empty(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()