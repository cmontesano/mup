import contextlib
import errno
import logging
import os
import shutil
import stat
import tempfile

logger = logging.getLogger(__name__)


def handle_remove_readonly(func, path, exc):
    exc_value = exc[1]
    if func in (os.rmdir, os.remove, os.unlink):
        if exc_value.errno == errno.EACCES:
            if func is not os.rmdir:
                # make sure parent folder is writable
                parent_path = os.path.dirname(path)
                os.chmod(parent_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            func(path)
            return
    raise


@contextlib.contextmanager
def temp_path():
    tmp_dir = tempfile.mkdtemp()
    logger.debug(f"created temp folder {tmp_dir}")
    try:
        yield tmp_dir
    finally:
        logger.debug(f"removing temp folder {tmp_dir}")
        shutil.rmtree(tmp_dir, onerror=handle_remove_readonly)
