import unittest
from blocknodes import BlockType,markdown_to_blocks,block_to_block_type,markdown_to_html_node

class TestBlockNodes(unittest.TestCase):
    def test_single_word_paragraph(self):
        block = "just a regular sentence"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)



    def test_single_word_heading(self):
        block = "# hehe"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.HEADING)

    def test_3_word_heading(self):
        block = "### hehe"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.HEADING)

    def test_multiline_codeblocks(self):
        block = """``` 
        hehe kocham pilke
        jem parowki
        KFC > McDonald bo wiecej bialka w kurczakach
        
        ```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.CODE)
    def test_quote(self):
        block = """> hehe 
> hehe x2
> hehe x3
> hehe x4
>hehex5"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.QUOTE)

    def test_ordered_list(self):
        block = """1. Jem Chleb
2. I eat dirt
3. Buhahaahahaha"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.ORDERED_LIST)
        
    def test_unordered_list(self):
        block = """- OnePiece kiedys szacun dzisiaj mid
- BlackClover teraz to peak
- Made in Abyss stworzyla dziwna osoba (nie gadajmy o tym)"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type,BlockType.UNORDERED_LIST)

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )