class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        re_string = "" #return string
        if self.props:
            for prop in self.props.keys():
                re_string += f" {prop}=\"{self.props[prop]}\""
        return re_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        html_props = self.props_to_html()
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"