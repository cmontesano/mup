import enum
import fnmatch
import logging
import os
import random
import re
import string

from typing import Generator, Sequence, Union

from .temp_path import temp_path

__all__ = ['create_directories', 'find_files', 'get_unique_name', 'UniqueMode', 'temp_path']

logger = logging.getLogger(__name__)

RAND_CHARS = string.ascii_letters + string.digits


class UniqueMode(enum.Enum):
    RANDOM = 0
    INTEGER = 1


def create_directories(path: str, *, is_file: bool = False):
    if is_file:
        path = os.path.dirname(path)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def find_files(path: str, patterns: Union[str, Sequence], *, recursive: bool = False) -> Generator[str, None, None]:
    if isinstance(patterns, str):
        patterns = [patterns]
    pattern_regex = re.compile('|'.join([fnmatch.translate(p) for p in patterns]))

    if recursive:
        for root, dirs, files in os.walk(path):
            for f in files:
                if pattern_regex.match(f):
                    yield os.path.join(root, f)
    else:
        for item in os.scandir(path):
            if pattern_regex.match(item.name):
                yield item.path


def get_unique_name(path: str, *, mode: UniqueMode = UniqueMode.RANDOM, **kwargs) -> str:
    delimiter = kwargs.get('delimiter', "-")
    max_iterations = kwargs.get("max_iterations", 9999)
    force_unique = kwargs.get("force", False)

    if mode == UniqueMode.RANDOM:
        length = kwargs.get("length", 8)

        def unique_key_fn(_: int) -> str:
            return "".join(random.choices(RAND_CHARS, k=length))

    elif mode == UniqueMode.INTEGER:
        length = kwargs.get("length", 3)

        def unique_key_fn(iteration: int) -> str:
            return str(iteration).rjust(length, "0")

    else:
        raise NotImplementedError

    if not force_unique and not os.path.isfile(path):
        return path

    directory, file_name = os.path.split(path)
    file_name, extension = os.path.splitext(file_name)

    for i in range(max_iterations):
        unique_key = unique_key_fn(i + 1)
        new_file_name = f"{file_name}{delimiter}{unique_key}{extension}"
        check_path = os.path.join(directory, new_file_name)
        if not os.path.isfile(check_path):
            return check_path
