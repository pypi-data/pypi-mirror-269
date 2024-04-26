"""Environ"""

import os
import json
import datetime

from typing import Any, List, Tuple


EQUAL = '='
HASH = '#'


def _read_file(path: str, encoding: str) -> List[str]:
    """Read a file and return it as a list of strings"""

    with open(file=path, mode='r', encoding=encoding) as file:
        return file.read().splitlines()


def _parse_env_line(line: str, index_line: int) -> Tuple[str, str]:
    """Parses a line in the 'KEY=VALUE' format and returns the key (KEY) and the value (VALUE).

    Args:
        line (str): The line in the 'KEY=VALUE' format to parse.
        index_line (int): The index of the line in the file.

    Returns:
        Tuple[str, str]: A tuple with the key (KEY) and the value (VALUE) obtained from the line.

    Raises:
        SyntaxError: If the key-value syntax is invalid or the key is not defined.
    """

    if line.count(EQUAL) != 1:
        raise SyntaxError(
            f'On line {index_line}, the key-value syntax is invalid.')

    key, value = line.split(EQUAL)

    if not key:
        raise SyntaxError(
            f'The key has not been defined on line {index_line}.')

    return key, value


def read_environ(path: str = '.env', encoding: str = 'utf-8'):
    """
    Reads a .env file and sets the environment variables accordingly.

    Args:
        path (str, optional): The path to the .env file. Defaults to '.env'.
        encoding (str, optional): The encoding of the file. Defaults to 'utf-8'.

    Raises:
        IOError: If the file cannot be read.
    """
    file_content = _read_file(
        path=path,
        encoding=encoding)

    for index, line in enumerate(file_content):
        if line.startswith(HASH) or not line:
            continue

        key, value = _parse_env_line(line=line, index_line=index + 1)
        os.environ[key] = value


class Env:
    """Class to handle environment variables.

    Usage:
        from grigodeenv2 import datetime, Env, read_environ

        read_environ('.env')

        env = Env(
            EMAIL_PORT=(int, 45),
            ANY_DATETIME=(datetime, None, {"format": '%d/%m/%y %H:%M:%S'})
        )

        SECRET_KEY = env('SECRET_KEY') # str
        DEBUG = env.bool('DEBUG') # bool
        SERVER_PORT = env.int('SERVER_PORT') #int
        EMAIL_PORT = env('EMAIL_PORT') #int
        HOSTS = env.list('HOSTS') # list
        ANY_DATETIME = env('ANY_DATETIME') # datetime
    """

    ENVIRON = os.environ

    def __init__(self, **kwars) -> None:
        self.schema = kwars

    def __call__(self, var: str, cast=str, default=None) -> str | None:
        return self.get_value(var, cast, default)

    def str(self, var: str, default=None, **kwars) -> str | None:
        """Returns the value as a str."""
        return self.get_value(var=var, cast=str, default=default, **kwars)

    def bytes(self, var: str, default=None, **kwars) -> bytes | None:
        """Returns the value as a bytes."""
        return self.get_value(var=var, cast=bytes, default=default, **kwars)

    def bool(self, var: str, default=None, **kwars) -> bool | None:
        """Returns the value as a bool.

        To indicate False, you must set the variable to False, false,
        or 0. Everything else is considered True.
        """
        return self.get_value(var=var, cast=bool, default=default, **kwars)

    def int(self, var: str, default=None, **kwars) -> int | None:
        """Returns the value as a int."""
        return self.get_value(var=var, cast=int, default=default, **kwars)

    def float(self, var: str, default=None, **kwars) -> float | None:
        """Returns the value as a float."""
        return self.get_value(var=var, cast=float, default=default, **kwars)

    def json(self, var: str, default=None, **kwars) -> Any | None:
        """Returns the value as a json."""
        return self.get_value(var=var, cast=json.loads, default=default, **kwars)

    def list(self, var: str, default=None, **kwars) -> List[Any] | None:
        """Returns the value as a list.

        You should define the lists as you would in JSON.
        """
        return self.get_value(var=var, cast=list, default=default, **kwars)

    def tuple(self, var: str, default=None, **kwars) -> Tuple[Any] | None:
        """Returns the value as a tuple.

        You should define tuples as you would define lists in JSON.
        """
        return self.get_value(var=var, cast=tuple, default=default, **kwars)

    def dict(self, var: str, default=None, **kwars) -> dict | None:
        """Returns the value as a dict."""
        return self.get_value(var=var, cast=dict, default=default, **kwars)

    def datetime(self, var: str, default=None,
                 _format='%d/%m/%y %H:%M:%S',
                 **kwars) -> datetime.datetime | None:
        """Returns the value as a datetime."""
        _kwars = {"format": _format}
        _kwars.update(kwars)
        return self.get_value(var=var, cast=datetime.datetime,
                              default=default, **_kwars)

    def get_value(self, var: str, cast=None, default=None, **kwars) -> Any | None:
        """Returns the value."""

        var_schema = self.schema.get(var)
        if var_schema is not None:
            len_var_schema = len(var_schema)

            if len_var_schema >= 1:
                cast = var_schema[0]
            if len_var_schema >= 2:
                default = var_schema[1]
            if len_var_schema >= 3:
                kwars = var_schema[2]

        value = self.ENVIRON.get(var)

        if value is None:
            return default

        return self.parse_value(var, value, cast, **kwars)

    def parse_value(self, var: str, value: str, cast=None, **kwars) -> Any:
        """Return the parsed value."""

        def to_bool(value: str, **_):
            if value in ('False', 'false', '0', ''):
                return False
            return True

        def to_list(value: str, **_):
            try:
                _list = json.loads(value)
            except json.decoder.JSONDecodeError as e:
                raise SyntaxError(
                    f"The syntax of variable '{var}' is invalid.") from e
            if isinstance(_list, list):
                return _list
            raise ValueError(f"The variable '{var}' is not a list.")

        def to_tuple(value: str, **_):
            return tuple(to_list(value))

        def to_datetime(value: str, **kwars):
            return datetime.datetime.strptime(value, kwars.get('format'))

        casts = {
            bool: to_bool,
            list: to_list,
            tuple: to_tuple,
            datetime.datetime: to_datetime,
        }

        if cast is None or not callable(cast):
            return None

        _cast = casts.get(cast)

        if _cast is None:
            return None

        cast = _cast

        return cast(value, **kwars)
