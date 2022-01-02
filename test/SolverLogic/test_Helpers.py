import unittest

from src.Solver import list_diff


class Test_Helper_Functions(unittest.TestCase):
    def test_list_diff(self):
        a = [1, 2, 2, 3, 4, 5, 5, 5, 6]
        b = [0, 1, 2, 3, 4, 5, 6, 7]
        expected = [2, 5, 5]
        actual = list_diff(a, b)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
