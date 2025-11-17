class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None, indents=[0,0], inline=False, self_closing=False):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.indents = indents
        self.inline = inline
        self.self_closing = self_closing

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props and not isinstance(self.props, dict):
            raise ValueError("props must be a dictionary\n\tProblem node: {self}")
        re_string = "" #return string
        if self.props:
            for prop in self.props.keys():
                re_string += f" {prop}=\"{self.props[prop]}\""
        return re_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None, indents=[0,0], inline=False, self_closing=False):
        super(LeafNode, self).__init__(tag, value, None, props, indents, inline, self_closing)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        html_props = self.props_to_html()
        if self.inline:
            if not self.tag:
                return self.value
            if not self.self_closing:
                return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{html_props}>{self.value}"
        else:
            if not self.tag:
                return self.value
            if not self.self_closing:
                return f"{leading_spaces(self.indents)}<{self.tag}{html_props}>{self.value}</{self.tag}>\n"
            else:
                return f"{leading_spaces(self.indents)}<{self.tag}{html_props}>{self.value}\n"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None, indents=[0,0], inline=False):
        if isinstance(children, HTMLNode):
            children = [children]
        super(ParentNode, self).__init__(tag, None, children, props, indents, inline)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag\n\tProblem node: {self}")
        if not self.children:
            raise ValueError(f"All parent nodes must have a child\n\tProblem node: {self}")
        if not isinstance(self.children, list):
            raise ValueError("children must be a list of HTMLNode instances\n\tProblem node: {self}")
        if not all(isinstance(c, HTMLNode) for c in self.children):
            raise ValueError("All children must be instances of HTMLNode\n\tProblem node: {self}")
        
        inner_html = ""
        html_props = self.props_to_html()
        for child in self.children:
            child.indents = [self.indents[0], self.indents[1] + 1] #Child should use the same indent spacing and be indented one level deeper
            if not isinstance(child, HTMLNode):
                raise ValueError("All children must be instances of HTMLNode\n\tProblem node: {self}\n\tInvalid child: {child}")
            inner_html += child.to_html()
        if inner_html.endswith("\n"):
            inner_html = inner_html[:-1]

        inner_indents = [self.indents[0], self.indents[1] + 1]
        if self.inline and (self.tag!="p" and self.tag!="blockquote"):
            return f"{leading_spaces(self.indents)}<{self.tag}{html_props}>{inner_html}</{self.tag}>\n"
        elif self.inline:
            return f"{leading_spaces(self.indents)}<{self.tag}{html_props}>\n{leading_spaces(inner_indents)}{inner_html}\n{leading_spaces(self.indents)}</{self.tag}>\n"
        return f"{leading_spaces(self.indents)}<{self.tag}{html_props}>\n{inner_html}\n{leading_spaces(self.indents)}</{self.tag}>\n"

def leading_spaces(indents):
    lead_spaces = " " * (indents[0] * indents [1])
    return lead_spaces