import logging
import os

from mup.proc import CommandRunner

logger = logging.getLogger(__name__)


def is_path_repository(path: str) -> bool:
    """ Check if a path contains a git repository. """
    return CommandRunner(cwd=path).run(("git", "rev-parse")).result == 0


def commit_id(path: str, *, short: bool = False) -> str:
    """ Fetch the current commit id (optionally the short version) from a git
     repository located at `path`. """
    command = ["git", "rev-parse"]
    if short:
        command.append("--short")
    command.append("HEAD")
    output = CommandRunner(cwd=path).run(command)
    if output.result == 0:
        return output.stdout.strip()
    raise RuntimeError(output.stderr)


def clone(url: str, *, destination: str, branch: str = "master") -> str:
    """ Clone a remote repository to `destination` and check out `branch`. This
    also mimics the behavior of creating a subfolder based on the name of the
    repository. """
    logger.info("Cloning repository %s", url)
    logger.debug("Repository branch %s", branch)
    logger.debug("Repository destination %s", destination)

    name = os.path.splitext(os.path.basename(url))[0]
    repo_path = os.path.join(destination, name)
    git_command = ("git", "clone", "-b", branch, url, repo_path)
    output = CommandRunner().run(git_command, silent=True)
    if output.result == 0:
        return repo_path
    raise RuntimeError(output.stderr)
