#!/usr/bin/env python3

# Standard libraries
from os import sep
from sys import platform, stdin, stdout

# Platform, pylint: disable=too-few-public-methods
class Platform:

    # Constants
    IS_LINUX: bool = platform in ['linux', 'linux2']
    IS_WINDOWS: bool = platform in ['win32', 'win64']

    # Separators
    PATH_SEPARATOR: str = sep

    # TTYs
    IS_TTY_STDIN: bool = stdin.isatty() and stdin.encoding != 'cp1252'
    IS_TTY_STDOUT: bool = stdout.isatty()
    IS_TTY_UTF8: bool = str(stdout.encoding).lower() == 'utf-8'

    # Flush
    @staticmethod
    def flush() -> None:

        # Flush output
        print('', end='', flush=Platform.IS_TTY_STDOUT)
