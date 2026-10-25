import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode('This is a text node', 2, None)")
    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        self.assertEqual(node.url, "https://example.com")
    def test_different_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a string, not a TextNode")

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="div", value="This is a div", children=None, props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=This is a div, children=None, props={'href': 'https://example.com', 'target': '_blank'})")
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="a", value="Click here")
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"class": "text"})
        self.assertEqual(node.props_to_html(), ' class="text"')
    def test_to_html_no_props(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2], props={"class": "container"})
        self.assertEqual(parent.props_to_html(), ' class="container"')
    def test_to_html_no_props(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.props_to_html(), "")
    def test_to_html_no_children(self):
        parent = HTMLNode(tag="div", children=None, props={"class": "container"})
        self.assertEqual(parent.props_to_html(), ' class="container"')
    def test_to_html_no_tag(self):
        parent = HTMLNode(tag=None, children=[HTMLNode(tag="span", value="Child 1")], props={"class": "container"})
        self.assertEqual(parent.props_to_html(), ' class="container"')

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_plain_text_node(self):
        text_node = TextNode("This is plain text", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is plain text")
    def test_bold_text_node(self):
        text_node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    def test_italic_text_node(self):
        text_node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
    def test_code_text_node(self):
        text_node = TextNode("print('Hello, World!')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, World!')")
    def test_link_text_node(self):
        text_node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props["href"], "https://example.com")
    def test_image_text_node(self):
        text_node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text")    

if __name__ == "__main__":
    unittest.main()