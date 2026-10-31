import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode,text_node_to_html_node,TextType,extract_markdown_images,extract_markdown_links,split_nodes_image
from textnode import split_nodes_link,text_to_textnodes
from blocknodes import markdown_to_blocks



class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        result = node.props_to_html()
        node2 = HTMLNode(tag="p",props={"href": "https://www.cwelandia.pl"})
        result2 = node2.props_to_html()
        node3 = HTMLNode(tag="p",props={"href": "https://www.kochamgrzyby.pl"})
        result3 = node3.props_to_html()
        self.assertEqual(result, " href=\"https://www.boot.dev\"")
        self.assertEqual(result2, " href=\"https://www.cwelandia.pl\"")
        self.assertEqual(result3, " href=\"https://www.kochamgrzyby.pl\"")

    def test_multiple_props(self):
        node4 = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node4.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_no_props(self):
        node5 = HTMLNode()
        self.assertEqual(node5.props_to_html(), "")

class TestHTMLNodeLeaf(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node6 = LeafNode("p", "Hello, world!")
        self.assertEqual(node6.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_prop(self):
        node7 = LeafNode("a","Click me!",{"href": "https://www.google.com"})
        self.assertEqual(node7.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")
    def test_leaf_no_value(self):
        node8 = LeafNode("a",None,{"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node8.to_html()
    def test_leaf_no_tag(self):
        node9 = LeafNode(None,"Eren please dont do this")
        self.assertEqual(node9.to_html(),"Eren please dont do this")

class TestHTMLParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node = LeafNode("i","David Martinez ratuj nightcity")
        grandchild_node2 = LeafNode("b","Capri dlaczego to zrobilas?")
        grandchild_node3 = LeafNode("a","Jestem odporny na chrom, chyba")
        child_node = ParentNode("section", [grandchild_node,grandchild_node2,grandchild_node3])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                                                "<div><section><i>David Martinez ratuj nightcity</i>"
                                                "<b>Capri dlaczego to zrobilas?</b>"
                                                "<a>Jestem odporny na chrom, chyba</a></section></div>"
                                                )

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_bold(self):
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

class TestTextImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestTextLink(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is paragraph with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)
            

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com/) and another [link](https://instagram.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://instagram.com/"),
            ],
            new_nodes,
        )

class TestTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)
        text2 = "This is _spanish_ word with a **strong** describtion in a `code block` and an ![image of goat](https://imgur.com/gallery/mmmm-salty-0Dd28Cd#/t/goats) and a [link](https://x.com/RaksoFN)"
        nodes2 = text_to_textnodes(text2)
        expected2 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("spanish", TextType.ITALIC),
            TextNode(" word with a ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" describtion in a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image of goat", TextType.IMAGE, "https://imgur.com/gallery/mmmm-salty-0Dd28Cd#/t/goats"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://x.com/RaksoFN"),
        ]
        self.assertListEqual(expected2,nodes2)

class TestMarkdownBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )




if __name__ == "__main__":
    unittest.main()
