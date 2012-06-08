import os.path
import unittest

from deduper.wrapper import GenericFileWrapper

from data import __file__ as data_module

data_dir = os.path.sep.join(data_module.split(os.path.sep)[:-1])

class TestWrapper(unittest.TestCase):
    def setUp(self):
        pass

    def test_hash(self):
        file1 = GenericFileWrapper(os.path.sep.join((data_dir, 'file1.txt')))
        file2 = GenericFileWrapper(os.path.sep.join((data_dir, 'file2.txt')))
        dif_file = GenericFileWrapper(os.path.sep.join((data_dir, 'different_file.txt')))

        self.assertEqual(file1, file2)
        self.assertEqual(file1.hash, file2.hash)
        self.assertNotEqual(file1.hash, None)

        self.assertNotEqual(file1, dif_file)
        self.assertNotEqual(file1.hash, dif_file.hash)
        self.assertEqual(file1.first_block_hash, dif_file.first_block_hash)
        self.assertNotEqual(dif_file.hash, None)

if __name__ == '__main__':
    unittest.main()
