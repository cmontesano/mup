import os
import pathlib
import shutil
import tempfile
import unittest

from mup.path import create_directories, find_files

FILES = (
    "file01.txt",
    "file02.py",
    "file03.sh",
    "1/file01.txt",
    "1/file02.py",
    "1/file03.sh",
    "1/1/file01.txt",
    "1/1/file02.py",
    "1/1/file03.sh",
    "1/1/1/file01.txt",
    "1/1/1/file02.py",
    "1/1/1/file03.sh",
    "2/file01.txt",
    "2/file02.py",
    "2/file03.sh",
    "2/2/file01.txt",
    "2/2/file02.py",
    "2/2/file03.sh",
    "2/2/2/file01.txt",
    "2/2/2/file02.py",
    "2/2/2/file03.sh",
)


class TestFindFiles(unittest.TestCase):
    tmp = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.mkdtemp()

        for f in FILES:
            path = os.path.join(cls.tmp, *f.split("/"))
            create_directories(path, is_file=True)
            pathlib.Path(path).touch()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp)

    def test_find_files(self):
        files = list(find_files(self.tmp, "*.txt"))
        self.assertEqual(len(files), 1)

    def test_find_files_recursive(self):
        files = list(find_files(self.tmp, "*.txt", recursive=True))
        self.assertEqual(len(files), 7)

    def test_find_files_recursive_multiple_patterns(self):
        files = list(find_files(self.tmp, ("*.txt", "*.py"), recursive=True))
        self.assertEqual(len(files), 14)
