from htmlnode import LeafNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        text_parts = old_node.text.split(delimiter)
        for i, part in enumerate(text_parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes
    
def extract_markdown_images(text) -> tuple():
    import re
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text) -> tuple():
    import re
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        last_index = 0
        for match in matches:
            alt_text, url = match
            start_index = old_node.text.find(f'![{alt_text}]({url})', last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(old_node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
            last_index = start_index + len(f'![{alt_text}]({url})')
        if last_index < len(old_node.text):
            new_nodes.append(TextNode(old_node.text[last_index:], TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        last_index = 0
        for match in matches:
            link_text, url = match
            start_index = old_node.text.find(f'[{link_text}]({url})', last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(old_node.text[last_index:start_index], TextType.PLAIN))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
            last_index = start_index + len(f'[{link_text}]({url})')
        if last_index < len(old_node.text):
            new_nodes.append(TextNode(old_node.text[last_index:], TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    # Use all the split functions to process the text and return a list of TextNode objects
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes