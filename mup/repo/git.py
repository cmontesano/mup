import logging
import os

from mup.proc import CommandRunner

logger = logging.getLogger(__name__)


def is_path_repository(path: str) -> bool:
    return CommandRunner(cwd=path).run(("git", "rev-parse")).result == 0


def commit_id(path: str, *, short: bool = False) -> str:
    command = ["git", "rev-parse"]
    if short:
        command.append("--short")
    command.append("HEAD")
    output = CommandRunner(cwd=path).run(command)
    if output.result == 0:
        return output.stdout.strip()
    raise RuntimeError(output.stderr)


def clone(url: str, *, destination: str, branch: str = "master") -> str:
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
