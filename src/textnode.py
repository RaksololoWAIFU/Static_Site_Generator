import re
from enum import Enum
from htmlnode import HTMLNode,LeafNode,ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "Code text"
    LINK = "link"
    IMAGE = "image"
    

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None,value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b",value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i",value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code",value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a",
                        value=text_node.text,
                        props={"href": text_node.url}
                        ) 
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text},
            )
    else:
        raise Exception(f"Invalid text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for x in old_nodes:
        if x.text_type != TextType.TEXT:
            new_list.append(x)
        else:
            parts = x.text.split(delimiter)
            if len(parts) % 2 != 1:
                raise Exception("invalid Markdown syntax")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_list.append(TextNode(part,TextType.TEXT))
                else:
                    new_list.append(TextNode(part,text_type))
    return new_list



def extract_markdown_images(text) -> list[tuple]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    results = re.findall(pattern,text)
    return results



def extract_markdown_links(text) -> list[tuple]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    results = re.findall(pattern,text)
    return results

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for x in old_nodes:
        if x.text_type == TextType.TEXT:
            check = extract_markdown_images(x.text)
            if len(check) == 0:
                new_list.append(x)
                continue
            reamining_text = x.text
            for alt_text, url in check:
                sections = reamining_text.split(f"![{alt_text}]({url})", 1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0],TextType.TEXT))
                new_list.append(TextNode(alt_text, TextType.IMAGE, url))
                reamining_text = sections[1]
            if reamining_text != "":
                new_list.append(TextNode(reamining_text, TextType.TEXT))

            
        else:
            new_list.append(x)
    return new_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for x in old_nodes:
        if x.text_type == TextType.TEXT:
            check = extract_markdown_links(x.text)
            if len(check) == 0:
                new_list.append(x)
                continue
            reamining_text = x.text
            for alt_text, url in check:
                sections = reamining_text.split(f"[{alt_text}]({url})", 1)
                if sections[0] != "":
                    new_list.append(TextNode(sections[0],TextType.TEXT))
                new_list.append(TextNode(alt_text, TextType.LINK, url))
                reamining_text = sections[1]
            if reamining_text != "":
                new_list.append(TextNode(reamining_text, TextType.TEXT))

            
        else:
            new_list.append(x)
    return new_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


