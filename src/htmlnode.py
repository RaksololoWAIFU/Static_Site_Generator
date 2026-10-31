

class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        empty = ""
        if self.props:
            for key,value in self.props.items():
                empty += f' {key}="{value}"'
            return empty
        else:
            return empty

    def __repr__(self):
        return f"{self.tag},{self.value},{self.children},{self.props}"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"{self.tag},{self.value},{self.props}"    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)

    
    def to_html(self):
        if not self.tag:
            raise ValueError
        if self.children is None:
            raise ValueError("children is missing")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()


        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"