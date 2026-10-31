from enum import Enum
from htmlnode import HTMLNode,LeafNode,ParentNode
import re
from textnode import text_node_to_html_node,text_to_textnodes,TextType,TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        clean_block = block.strip()
        if clean_block != "":
            blocks.append(clean_block)
    return blocks

def block_to_block_type(block)-> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    
    if lines[0].startswith(("```")) and lines[-1].endswith(("```")) and len(lines) > 1:
        return BlockType.CODE
    
    is_it_quote = True
    for x in lines:
        if not x.startswith((">")):
            is_it_quote = False
            break
    if is_it_quote:
        return BlockType.QUOTE
    
    is_it_unordered_list = True
    for y in lines:
        if not y.startswith(("- ")):
            is_it_unordered_list = False
            break
    if is_it_unordered_list:
        return BlockType.UNORDERED_LIST
    
    is_it_ordered_list = True
    i=0
    for o in lines:
        i+=1

        if not o.startswith((f"{i}. ")):
            is_it_ordered_list = False
            break
    if is_it_ordered_list:
        return BlockType.ORDERED_LIST
    if not is_it_ordered_list:
        return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        noder = text_node_to_html_node(node)
        children.append(noder)
    return children

def helper_paragraph(markdown):
    raw = markdown.split("\n")
    joined = " ".join(raw)
    children = text_to_children(joined)
    return ParentNode("p", children)

def helper_heading(markdown):
    level = 0
    for char in markdown:
        if char == "#":
            level += 1
        else:
            break
    text = markdown[level+1:]
    children = text_to_children(text)
    dynamic_tag = f"h{level}"
    return ParentNode(dynamic_tag,children)

def helper_code(markdown):
    strip = markdown[3:-3]
    node = TextNode(strip, TextType.CODE, url=None)
    convert = text_node_to_html_node(node)
    
    return ParentNode("pre", [convert])

def helper_quote(markdown):
    split = markdown.split("\n")
    empty_list = []
    for x in split:
        stripped =  x.lstrip("> ")
        empty_list.append(stripped)
    full_list = " ".join(empty_list)
    children = text_to_children(full_list)
    return ParentNode("blockquote", children)

def helper_unordered_lits(markdown):
    split = markdown.split("\n")
    empty_list = []
    for x in split:
        stripped = x.lstrip("- ")
        children = text_to_children(stripped)
        wrapped = ParentNode("li", children)
        empty_list.append(wrapped)
    return ParentNode("ul", empty_list)

def helper_ordered_lits(markdown):
    split = markdown.split("\n")
    empty_list = []
    count = 0
    for x in split:
        count += 1
        prefix = f"{count}. "
        stripped = x.replace(prefix,"")
        children = text_to_children(stripped)
        wrapped = ParentNode("li", children)
        empty_list.append(wrapped)
    return ParentNode("ol", empty_list)


    
    
        
def markdown_to_html_node(markdown) -> HTMLNode:
    block = markdown_to_blocks(markdown)
    empty_list = []
    for x in block:
        what_is_it = block_to_block_type(x)
        if what_is_it == BlockType.PARAGRAPH:
            html_node = helper_paragraph(x)
            empty_list.append(html_node)
        elif what_is_it == BlockType.HEADING:
            html_node2 = helper_heading(x)
            empty_list.append(html_node2)
        elif what_is_it == BlockType.CODE:
            html_node3 = helper_code(x)
            empty_list.append(html_node3)
        elif what_is_it == BlockType.QUOTE:
            html_node4 = helper_quote(x)
            empty_list.append(html_node4)
        elif what_is_it == BlockType.UNORDERED_LIST:
            html_node5 = helper_unordered_lits(x)
            empty_list.append(html_node5)
        elif what_is_it == BlockType.ORDERED_LIST:
            html_node6 = helper_ordered_lits(x)
            empty_list.append(html_node6)
    return ParentNode("div", empty_list)       


