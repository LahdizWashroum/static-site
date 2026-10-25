from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6
    STRIKETHROUGH = 7
    SPOILER = 8
    HIGHLIGHT = 9
    UNDERLINE = 10

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value}, {self.url!r})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.STRIKETHROUGH:
        return LeafNode(tag="s", value=text_node.text)
    elif text_node.text_type == TextType.SPOILER:
        return LeafNode(tag="span", value=text_node.text, props={"class": "spoiler"})
    elif text_node.text_type == TextType.HIGHLIGHT:
        return LeafNode(tag="mark", value=text_node.text)
    elif text_node.text_type == TextType.UNDERLINE:
        return LeafNode(tag="u", value=text_node.text)
    raise ValueError(f"Unsupported text type: {text_node.text_type}")