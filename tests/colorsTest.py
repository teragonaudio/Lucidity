import unittest
from lucidity.colors import ColorChooser

class ColorsTests(unittest.TestCase):
    def test_create_empty_chooser(self):
        c = ColorChooser()
        self.assertEqual(len(c._colorList), 0)

    def test_empty_chooser_random_color(self):
        c = ColorChooser()
        self.assertEqual(c.randomColor(), ColorChooser.DEFAULT_COLOR)

    def test_empty_chooser_next_color(self):
        c = ColorChooser()
        self.assertEqual(c.nextColor(), ColorChooser.DEFAULT_COLOR)
        self.assertEqual(c.nextColor(), ColorChooser.DEFAULT_COLOR)

    def test_empty_chooser_find_color(self):
        c = ColorChooser()
        self.assertEqual(c.findColor("Red"), ColorChooser.DEFAULT_COLOR)

    def test_create_from_file(self):
        c = ColorChooser.createFromDefinition("resources/colortest.txt")
        self.assertEqual(len(c._colorList), 3)
        self.assertEqual(c.findColor("First Color"), (255, 0, 0))
        self.assertEqual(c.findColor("Other Color"), (0, 255, 0))
        self.assertEqual(c.findColor("Third Color"), (0, 0, 255))
        self.assertEqual(c.currentColor(), (255, 0, 0))
        self.assertEqual(c.nextColor(), (0, 255, 0))
        self.assertEqual(c.nextColor(), (0, 0, 255))

    def test_interval(self):
        c = ColorChooser.createFromDefinition("resources/colortest.txt")
        self.assertEqual(c.currentColor(), (255, 0, 0))
        self.assertEqual(c.nextColor(2), (0, 0, 255))

    def test_find_invalid_color(self):
        c = ColorChooser()
        self.assertEqual(c.findColor("invalid"), ColorChooser.DEFAULT_COLOR)

    def test_read_hex_colors(self):
        line = "Red: #ff0000"
        result = ColorChooser.colorFromLine(line)
        self.assertNotEqual(result, None)
        self.assertEqual(result[0], "Red")
        self.assertEqual(result[1], (255, 0, 0))

if __name__ == '__main__':
    unittest.main()
