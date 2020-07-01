import logging
import os
import subprocess

from collections import namedtuple
from typing import List, Sequence, Union


CommandResult = namedtuple("CommandResult", ["result", "stdout", "stderr"])

logger = logging.getLogger(__name__)


class CommandRunner(object):
    def __init__(self, **kwargs):
        self.cwd = kwargs.get('cwd', os.getcwd())
        self.env = kwargs.get('env', os.environ.copy())

    def _split_path_var(self, key: str) -> List[str]:
        values = self.env.get(key, "").split(os.pathsep)
        return [v for v in values if len(v.strip())]

    def env_path_append(self, key: str, value: str):
        values = self._split_path_var(key)
        values.append(value)
        self.env[key] = os.pathsep.join(values)

    def env_path_prepend(self, key: str, value: str):
        values = self._split_path_var(key)
        values.insert(0, value)
        self.env[key] = os.pathsep.join(values)

    def env_var_add(self, key: str, value: str):
        self.env[key] = value

    def env_var_remove(self, key: str):
        try:
            del self.env[key]
        except KeyError:
            pass

    def run(self, command: Union[bytes, str, Sequence], **kwargs) -> CommandResult:
        env = kwargs.get('env', self.env)

        subprocess_args = {
            'cwd': kwargs.get('cwd', self.cwd),
            'env': env,
            'shell': False,
            'universal_newlines': True,
            'encoding': 'utf8',
        }

        silent = kwargs.get('silent', True)
        if silent:
            subprocess_args['stdout'] = subprocess.PIPE
            subprocess_args['stderr'] = subprocess.PIPE

        logger.debug("Running command %s", str(command))
        logger.debug("Command environment %s", str(env))
        logger.debug("Command working directory %s", subprocess_args['cwd'])
        proc = subprocess.Popen(command, **subprocess_args)
        result = proc.wait()

        if silent:
            return CommandResult(result, proc.stdout.read(), proc.stderr.read())
        else:
            return CommandResult(result, None, None)
