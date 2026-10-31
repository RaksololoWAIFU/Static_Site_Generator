import unittest
from gencontent import extract_title

class Test_Headers(unittest.TestCase):
    def test_headerh1(self):
        text = extract_title("# Hello")
        self.assertEqual(text, "Hello")

    def test_headerh1_seperate(self):
        text = extract_title("""Hello my name is mrcrab\n# nice to meet you""")
        self.assertEqual(text, "nice to meet you")

    def test_headerh1_wrong(self):
        text = "Hello I'm just a simple guy\nI love chicken wings but my stomach says no"
        with self.assertRaises(Exception):
            extract_title(text)