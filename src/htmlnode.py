
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("Subclasses must implement the to_html method.")
    def props_to_html(self):
        if not self.props:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    def to_html(self):
        if self.value is None:
            if self.tag == "img":
                return f"<img{self.props_to_html()}>"
            raise ValueError("LeafNode must have a value to convert to HTML.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag=tag, value=value, children=children, props=props)
    def to_html(self):
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML.")
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML.")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"