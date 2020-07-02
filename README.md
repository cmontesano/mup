# mup

Miscellaneous utility package for Python 3.7+.

## Usage

### mup.path.create_directories

Like `os.makedirs`, but will not error if the destination path already exists. You can also avoid using `os.path.dirname` by passing in a full file path and setting `is_file` to `True`.

```python
import os
import tempfile

from mup.path import create_directories

tmp_dir = tempfile.mkdtemp()
test_path = os.path.join(tmp_dir, "fake", "path", "here.txt")

create_directories(test_path, is_file=True)

assert os.path.isdir(os.path.dirname(test_path))
```

### mup.path.get_unique_name

Generate a unique file name by adding either random characters or sequential integers.

```python
from mup.path import get_unique_name, UniqueMode

file_path = "/path/to/file.txt"
delimiter = "-"

unique_path = get_unique_name(file_path, mode=UniqueMode.RANDOM, length=8, force=True, delimiter=delimiter)
assert len(unique_path) == len(file_path) + 8 + len(delimiter)

unique_path = get_unique_name(file_path, mode=UniqueMode.INTEGER, length=3, force=True, delimiter=delimiter)
assert len(unique_path) == len(file_path) + 3 + len(delimiter)

assert unique_path.endswith(f"file{delimiter}001.txt")
```

### mup.path.find_files

Search `path` for files, optionally *recursively*, and yield files that match `pattern`.

Note that `pattern` expects an `fnmatch` compatible pattern (e.g. `*.py`), or a list/tuple of patterns.

```python
import os

from mup.path import find_files

for f in find_files(os.path.expanduser("~"), "*.py"):
    print(f"Found python file '{f}' in home directory.")
```

### mup.path.temp_path

Context manager to create a temporary path and clean it up automatically.

```python
import os

from mup.path import temp_path

with temp_path() as tmp:
    assert os.path.isdir(tmp)

assert not os.path.isdir(tmp)

```

### mup.proc.open_file

A basic attempt at a cross platform version of `os.startfile`.

```python
from mup.proc import open_file

open_file("file.txt")
```

### mup.proc.CommandRunner

A wrapper around `subprocess.Popen` with basic environment manipulation. The results of a subprocess operation will be returned as a `CommandResult` object, which includes the return code, and stdout/stderr. Note that stdout/stderr will only be populated if the command was run silently.

```python
import os

from mup.proc import CommandRunner

c = CommandRunner(env={})
c.env_var_add("TEST", "1234")
assert c.env['TEST'] == '1234'

if os.name == "nt":
    command = "set"
elif os.name == "posix":
    command = "printenv"

result = c.run(command, silent=True)
assert result.result == 0
assert result.stdout.count("TEST=1234") == 1
```

### mup.repo.git.is_path_repository

Check if a path contains a git repository.

```python
import os
from mup.repo.git import is_path_repository

repo_path = os.path.expanduser("~/repository")

if is_path_repository(repo_path):
    print(f"'{repo_path}' is a git repository")
else:
    print(f"'{repo_path}' is not a git repository")
```

### mup.repo.git.commit_id

Fetch the current commit id (optionally the short version) from a git repository located at `path`.

```python
import os
from mup.repo.git import commit_id

repo_path = os.path.expanduser("~/repository")

short_id = commit_id(repo_path, short=True)
full_id = commit_id(repo_path, short=False)
```

### mup.repo.git.clone

Clone a remote repository to `destination` and check out `branch`. This also mimics the behavior of creating a subfolder based on the name of the repository.

```python
import os
from mup.repo.git import clone

repositories = os.path.expanduser("~/repositories")

repo_path = clone("https://address/of/remote/repository.git", destination=repositories)
print(f"repository cloned to {repo_path}")
```
