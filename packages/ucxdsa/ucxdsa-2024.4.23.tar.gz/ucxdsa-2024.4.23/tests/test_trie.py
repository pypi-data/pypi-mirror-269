import unittest
import sys

from dsa.trie import Trie

class TestTrie(unittest.TestCase):
    def test_all(self):
        t = Trie()

        t.insert("python")
        t.insert("python")
        t.insert("pygame")
        t.insert("pandas")
        t.insert("apple")

        self.assertIsNotNone(t.search("python"))
        self.assertIsNotNone(t.search("pygame"))
        self.assertIsNotNone(t.search("apple"))
        self.assertIsNotNone(t.search("py"))
        t.delete("python")
        self.assertIsNone(t.search("python"))

        # autocomplete
        words = t.autocomplete("a")
        self.assertEqual(len(words), 1)
        words = t.autocomplete("apple")
        self.assertEqual(len(words), 1)
        words = t.autocomplete("Apple")
        self.assertIsNone(words, 0)

        words = t.autocomplete("p")
        self.assertEqual(len(words), 2)
        words = t.autocomplete("py")
        self.assertEqual(len(words), 1)
        t.insert("python")
        words = t.autocomplete("py")
        self.assertEqual(len(words), 2)

        # suggest
        words = t.suggest("abc")
        self.assertEqual(words[0], "apple")

        words = t.suggest("p")
        self.assertEqual(len(words), 3)

        words = t.suggest("paper")
        self.assertEqual(words[0], "pandas")
