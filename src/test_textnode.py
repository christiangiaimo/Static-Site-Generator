import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_delimiter import *
from extract_links import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
                                    TextNode("This is text with a ", TextType.TEXT),
                                    TextNode("code block", TextType.CODE),
                                    TextNode(" word", TextType.TEXT),
                                    ])

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[
                                    TextNode("This is text with a ", TextType.TEXT),
                                    TextNode("bold block", TextType.BOLD),
                                    TextNode(" word", TextType.TEXT),
                                    ])

    def test_split_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,[
                                    TextNode("This is text with a ", TextType.TEXT),
                                    TextNode("italic block", TextType.ITALIC),
                                    TextNode(" word", TextType.TEXT),
                                    ])    

    def test_split_delimiter_exception(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("This is text with a _italic block word", TextType.TEXT)
            split_nodes_delimiter([node], "?", TextType.ITALIC)
            

    def test_split_delimiter_italic(self):
        node = TextNode("This is text with a **BOLD** block_ word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[
                                    TextNode("This is text with a **BOLD** block_ word", TextType.BOLD),
                                    ])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                                        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                                            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                                        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
                                            )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_extract_link_exception(self):
        with self.assertRaises(Exception) as cm:
            extract_markdown_links("This is no a valid link https://www.google.com")


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
                            TextNode(
                                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                            ),
                            ],
                            new_nodes,
                            )
        

    def test_split_links(self):
        node = TextNode(
                        "This is text with an ![link](https://www.google.com) and another ![second link](https://i.imgur.com)",
                        TextType.TEXT,
                        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                            [
                            TextNode("This is text with an ", TextType.TEXT),
                            TextNode("link", TextType.IMAGE, "https://www.google.com"),
                            TextNode(" and another ", TextType.TEXT),
                            TextNode(
                                    "second link", TextType.IMAGE, "https://i.imgur.com"
                            ),
                            ],
                            new_nodes,
                            )
        




    def test_convert_to_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_nodes(text)
        self.assertListEqual([
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
                            ],new_nodes)


    
if __name__ == "__main__":
    unittest.main()
