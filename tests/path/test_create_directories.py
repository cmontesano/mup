import os
import unittest

from mup.path import temp_path
from mup.path import create_directories


class TestCreateDirectories(unittest.TestCase):
    def test_create_directories(self):
        with temp_path() as tmp:
            nested_path = os.path.join(tmp, "1", "2", "3", "4", "5")
            create_directories(nested_path)
            self.assertTrue(os.path.isdir(nested_path))
            try:
                create_directories(nested_path)
            except FileExistsError:
                self.fail("This should never happen")

    def test_create_directories_file(self):
        with temp_path() as tmp:
            nested_path = os.path.join(tmp, "1", "2", "3", "4", "5")
            create_directories(nested_path, is_file=True)
            self.assertFalse(os.path.isdir(nested_path))
            self.assertTrue(os.path.isdir(os.path.dirname(nested_path)))
