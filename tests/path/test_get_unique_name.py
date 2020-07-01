import os
import pathlib
import unittest

from mup.path import temp_path
from mup.path import get_unique_name, UniqueMode


# noinspection DuplicatedCode
class TestGetUniqueName(unittest.TestCase):
    def test_get_unique_name_random(self):
        with temp_path() as tmp:
            for _ in range(10):
                file_path = get_unique_name(os.path.join(tmp, "file.txt"),
                                            mode=UniqueMode.RANDOM)
                pathlib.Path(file_path).touch()
            self.assertEqual(len(os.listdir(tmp)), 10)

    def test_get_unique_name_integer(self):
        with temp_path() as tmp:
            for _ in range(10):
                file_path = get_unique_name(os.path.join(tmp, "file.txt"),
                                            mode=UniqueMode.INTEGER)
                pathlib.Path(file_path).touch()
            self.assertEqual(len(os.listdir(tmp)), 10)

    def test_get_unique_name_bad_mode(self):
        with temp_path() as tmp:
            with self.assertRaises(NotImplementedError):
                # noinspection PyTypeChecker
                _ = get_unique_name(os.path.join(tmp, "file.txt"), mode=9999)

    def test_get_unique_name_force(self):
        with temp_path() as tmp:
            base_file = os.path.join(tmp, "file.txt")
            self.assertFalse(os.path.isfile(base_file))
            file_path = get_unique_name(base_file, mode=UniqueMode.INTEGER,
                                        length=4, delimiter="_", force=True)
            self.assertEqual(os.path.basename(file_path), "file_0001.txt")
