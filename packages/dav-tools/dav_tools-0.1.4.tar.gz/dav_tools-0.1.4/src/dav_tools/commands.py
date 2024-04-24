'''External command execution on local machine.'''

import platform as _platform
import subprocess as _subprocess
from shlex import split as _split
from subprocess import CalledProcessError
from typing import Callable as _Callable


def execute(command: str) -> bool:
    '''
    Run a command.

    :param command: the command to execute

    :returns: `True` if the command exits with return code zero, `False` otherwise
    '''
    exit_status = _subprocess.check_call(_split(command))
    return exit_status == 0

def get_output(command: str, on_success: _Callable[[bytes], any] = lambda x: x, on_error: _Callable[[], any] = None):
    '''
    Run a command and return its output.
    
    :param command: the command to execute

    :param on_success: call the specified function on the output before returning the data. Useful for casting the output from its original `bytes` format
    :param on_error: call the specified function if the command raised an exception. If this value is `None`, raises the exception.
    '''
    try:
        return on_success(_subprocess.check_output(_split(command)))
    except CalledProcessError as e:
        if on_error is None:
            raise e
        return on_success(on_error())
    