import os
import tempfile
import unittest

from src.gen_emoji_xcompose import build, keysyms, parse_custom, parse_gemoji, parse_wincompose, read_custom


class GenTest(unittest.TestCase):
    def test_keysyms(self):
        self.assertEqual(keysyms("+1"), ["plus", "1"])
        self.assertEqual(keysyms("a b"), ["a", "space", "b"])
        self.assertIsNone(keysyms("café"))

    def test_line_format(self):
        self.assertEqual(build([("sob", "😭")]),
                         ['<Multi_key> <Multi_key> <s> <o> <b> : "😭" # sob'])

    def test_length_cap(self):
        self.assertEqual(build([("tableflip", "x")]), [])
        self.assertEqual(len(build([("abcdefgh", "x")])), 1)

    def test_prefix_keeps_shorter(self):
        self.assertEqual([l.split("# ")[1] for l in build([("flipper", "🐬"), ("flip", "x")])],
                         ["flip"])

    def test_very_short_prefix_yields(self):
        self.assertEqual([l.split("# ")[1] for l in build([("ok", "🆗"), ("ok_hand", "👌"), ("+1", "👍")])],
                         ["+1", "ok_hand"])

    def test_first_entry_wins(self):
        self.assertIn('"custom"', build([("cat", "custom"), ("cat", "🐱")])[0])

    def test_escaping(self):
        self.assertIn(r'"a\"b\\c"', build([("q", 'a"b\\c')])[0])

    def test_parse_custom(self):
        text = "# comment\n\ntflip (╯°□°)╯︵ ┻━┻\nlenny ( ͡° ͜ʖ ͡°)\n"
        self.assertEqual(parse_custom(text), [("tflip", "(╯°□°)╯︵ ┻━┻"), ("lenny", "( ͡° ͜ʖ ͡°)")])

    def test_read_custom(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "custom.local.txt")
            self.assertEqual(read_custom(path), [])
            with open(path, "w", encoding="utf-8") as f:
                f.write("fight (ง •̀_•́)ง\n")
            self.assertEqual(read_custom(path), [("fight", "(ง •̀_•́)ง")])

    def test_parsers(self):
        self.assertEqual(parse_gemoji([{"emoji": "👍", "aliases": ["+1", "thumbsup"]}, {"aliases": ["x"]}]),
                         [("+1", "👍"), ("thumbsup", "👍")])
        line = '<Multi_key> <Multi_key> <o> <k> < > <h> <a> <n> <d> : "👌" U1F44C # ok hand'
        self.assertEqual(parse_wincompose(line), [("ok hand", "👌")])


if __name__ == "__main__":
    unittest.main()
