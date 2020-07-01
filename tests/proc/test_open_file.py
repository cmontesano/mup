import unittest

from unittest import mock

from mup.proc import open_file


class TestOpenFile(unittest.TestCase):
    @mock.patch('sys.platform', "win32")
    def test_open_file_win32(self):
        with mock.patch("os.startfile", create=True) as mock_startfile:
            open_file("testfile")
            self.assertTrue(mock_startfile.called)
            mock_startfile.assert_called_once_with("testfile")

    @mock.patch('sys.platform', "linux")
    def test_open_file_linux(self):
        with mock.patch("subprocess.call") as mock_call:
            open_file("testfile")
            self.assertTrue(mock_call.called)
            mock_call.assert_called_once_with(["xdg-open", "testfile"])

    @mock.patch('sys.platform', "darwin")
    def test_open_file_darwin(self):
        with mock.patch("subprocess.call") as mock_call:
            open_file("testfile")
            self.assertTrue(mock_call.called)
            mock_call.assert_called_once_with(["open", "testfile"])
