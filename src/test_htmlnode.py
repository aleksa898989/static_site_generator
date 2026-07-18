import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "This is a paragraph", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("img", None, None, {"src": "image.png"})
        self.assertEqual(node.props_to_html(), ' src="image.png"')

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "This is a paragraph")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph", None, {"class": "text"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, This is a paragraph, None, {'class': 'text'})",
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            None,
            [HTMLNode("p", "child")],
            None,
        )
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.props)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

    def test_leaf_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertIsNone(node.children)


class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [ParentNode("div", [LeafNode("b", "deep")])],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><div><div><b>deep</b></div></div></div>",
        )

    def test_parent_repr(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("div", [child_node])
        self.assertEqual(
            repr(node), f"ParentNode(div, [{child_node!r}], None)"
        )


if __name__ == "__main__":
    unittest.main()
