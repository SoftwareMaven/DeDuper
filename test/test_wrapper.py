import os.path
import unittest

from deduper.wrapper import FileWrapper

from data import __file__ as data_module

data_dir = os.path.sep.join(data_module.split(os.path.sep)[:-1])

class TestWrapper(unittest.TestCase):
    def setUp(self):
        pass

    def test_hash(self):
        file1 = FileWrapper(data_dir, 'file1.txt')
        file2 = FileWrapper(data_dir, 'file2.txt')
        dif_file = FileWrapper(data_dir, 'different_file.txt')

        self.assertEqual(file1, file2)
        self.assertEqual(file1.hash, file2.hash)
        self.assertNotEqual(file1.hash, None)

        self.assertNotEqual(file1, dif_file)
        self.assertNotEqual(file1.hash, dif_file.hash)
        self.assertNotEqual(dif_file.hash, None)

if __name__ == '__main__':
    unittest.main()
