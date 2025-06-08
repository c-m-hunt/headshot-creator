import unittest

from .utils import add_padding


class AddPadding(unittest.TestCase):
    def test_returns_correct_with_no_padding_for_square_image(self):
        x1, y1, x2, y2 = add_padding(5, 5, 10, 10, (0, 0), 1)

        self.assertEqual(x1, 5)
        self.assertEqual(x2, 15)
        self.assertEqual(y1, 5)
        self.assertEqual(y2, 15)

    def test_returns_correct_with_no_padding(self):
        x1, y1, x2, y2 = add_padding(5, 5, 10, 10, (0, 0), 1.5)

        self.assertEqual(x1, 2)
        self.assertEqual(x2, 17)
        self.assertEqual(y1, 5)
        self.assertEqual(y2, 15)

    def test_adds_basic_padding(self):
        x1, y1, x2, y2 = add_padding(50, 50, 100, 100, (0.1, 0.2), 1.5)

        self.assertEqual(y1, 40)
        self.assertEqual(y2, 170)
        self.assertEqual(x1, 2)
        self.assertEqual(x2, 197)

