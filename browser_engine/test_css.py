import unittest
from css_resolver import Node, Rule, StyleResolver, compute_specificity, match_selector

class TestCSSResolver(unittest.TestCase):
    def test_selector_matching(self):
        node = Node("div", {"id": "main", "class": "container active"})
        self.assertTrue(match_selector(node, "div"))
        self.assertTrue(match_selector(node, "#main"))
        self.assertTrue(match_selector(node, ".container"))
        self.assertTrue(match_selector(node, ".active"))
        self.assertTrue(match_selector(node, "div.container"))
        self.assertFalse(match_selector(node, "p"))
        self.assertFalse(match_selector(node, ".inactive"))

    def test_specificity_dummy(self):
        # Testing if helper exists (will fail if unimplemented during checkpoint)
        spec = compute_specificity("div")
        self.assertEqual(len(spec), 3)

if __name__ == '__main__':
    unittest.main()
