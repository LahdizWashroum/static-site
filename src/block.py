from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline import text_to_textnodes
from textnode import text_node_to_html_node


def _inline_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block: str) -> BlockType:
    stripped_block = block.strip()
    if stripped_block.startswith('#'):
        return BlockType.HEADING
    elif stripped_block.startswith('```'):
        return BlockType.CODE
    elif stripped_block.startswith('>'):
        return BlockType.QUOTE
    elif stripped_block.startswith('- '):
        return BlockType.UNORDERED_LIST
    elif stripped_block[0].isdigit() and stripped_block[1:3] == '. ':
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown) -> list[str]:
    blocks = markdown.split('\n\n')
    result = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            result.append(stripped_block)
    return result

def markdown_to_html_nodes(markdown: str) -> list[tuple[BlockType, ParentNode]]:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append((block_type, ParentNode(tag="p", children=_inline_children(block))))
        elif block_type == BlockType.HEADING:
            heading_level = len(block.split(' ')[0])  # Count the number of '#' characters
            html_nodes.append((block_type, ParentNode(tag=f"h{heading_level}", children=_inline_children(block[heading_level:].strip()))))
        elif block_type == BlockType.CODE:
            code_content = block.strip('`')
            html_nodes.append((block_type, ParentNode(tag="pre", children=[ParentNode(tag="code", children=[LeafNode(tag=None, value=code_content)])])))
        elif block_type == BlockType.QUOTE:
            quote_content = block.lstrip('>').strip()
            html_nodes.append((block_type, ParentNode(tag="blockquote", children=_inline_children(quote_content))))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [item.strip('- ').strip() for item in block.split('\n')]
            html_nodes.append((block_type, ParentNode(tag="ul", children=[ParentNode(tag="li", children=_inline_children(item)) for item in list_items])))
        elif block_type == BlockType.ORDERED_LIST:
            list_items = [item.split('. ', 1)[1].strip() for item in block.split('\n')]
            html_nodes.append((block_type, ParentNode(tag="ol", children=[ParentNode(tag="li", children=_inline_children(item)) for item in list_items])))
    return html_nodes