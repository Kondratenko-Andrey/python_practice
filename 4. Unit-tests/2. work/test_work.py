from work import *
import unittest

data = {
    'Смартфон': 251,
    'Компьютер': 340,
    'Планшет': 36,
    'ТВ': 10
}


class TestWork(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test_arr(self):
        self.assertTrue(isinstance(test_arr(data), tuple))

    def test_percent1(self):
        self.assertEqual(type(percent([4, 54, 324, 5, 6])),
                         list)

    def test_percent2(self):
        with self.assertRaises(TypeError):
            percent(['Смартфон', 'Компьютер', 'Планшет', 'ТВ'])

    def test_percent3(self):
        for i in percent([13, 256, 56]):
            with self.subTest(i=i):
                self.assertGreaterEqual(100.0, i)


if __name__ == '__main__':
    unittest.main()
