from collections import namedtuple
from typing import Dict, Iterator, List, Match

import io
import re

class Template:

    # variables and types
    _tokens: Dict[str, str]
    _token_pattern: str
    _file: io.TextIOWrapper

    # constructors

    def __init__(self, token_pattern: str = '\\$\\{[a-zA-Z]*\\}') -> None:
        self._tokens = {
            "${Global}": []
        }

        self._token_pattern = token_pattern
        self._file = None

    def __del__(self):
        if self._file_is_open():
            self._file.close()

    # public
    
    def load(self, path: str) -> None:
        if self._file_is_open():
            self._file.close()

        self._file = open(path, 'r')
        self._file.seek(0)

    def scan(self) -> None:
        if not self._file_is_open():
            msg = 'Not loaded template file, call load() first'
            raise FileNotFoundError(msg)

        self._file.seek(0)
        for line in self._file:
            # get the token
            tokens = Template._scan_line(self._token_pattern, line)

            # add each token
            for token in tokens:
                self._add_token(token)

    def replace(self, key: str, replacement: str) -> None:
        if key in self._tokens:
            for token in self._tokens[key]:
                token = replacement

    def render(self) -> io.StringIO:
        rendered: io.StringIO = ''

        self._file.seek(0)
        for line in self._file:
            tmp: str = line

            for key in self._tokens.keys:
                tmp = tmp.replace(key, self._tokens[key])

        return rendered

    # private

    def _file_is_open(self) -> bool:
        return (self._file is not None and not self._file.closed)

    def _scan_line(token_pattern: str, line: str) -> Iterator[Match]:
        return re.finditer(token_pattern, line)

    def _add_token(self, match: Match):
        key = match.group(0)

        # create the list for the key
        if key not in self._tokens:
            self._tokens[key] = ''
