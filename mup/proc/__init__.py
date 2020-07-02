import os
import subprocess
import sys

from .command_runner import CommandRunner, CommandResult


def open_file(filename):
    """ A basic attempt at a cross platform version of `os.startfile`. """
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
