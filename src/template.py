from collections import namedtuple
from typing import Dict, List, Match

import io
import re


class Template:

    # token contains it's start and end positions in the file
    Token = namedtuple("Token", "start end")
    _tokens: Dict[str, List[Token]]
    _token_pattern: str
    _file: io.TextIOWrapper

    def __init__(self, token_pattern: str = '\\$\\{[a-zA-Z]*\\}') -> None:
        self._tokens = {
            "global": []
        }

        self._token_pattern = token_pattern
        self._file = None

    def __del__(self):
        if self._file_is_open():
            self._file.close()

    def _file_is_open(self) -> bool:
        return (self._file is not None and not self._file.closed)

    def load(self, path: str):
        if self._file_is_open():
            self._file.close()

        self._file = open(path, 'r')

    def scan(self):
        if not self._file_is_open():
            msg = 'Not loaded template file, call load() first'
            raise FileNotFoundError(msg)

        for line in self._file:
            tokens = self.scan_line(line, self._token_pattern)

            for token in tokens:
                self.add_token(token)

    def scan_line(line: str, token_pattern: str):
        return re.finditer(token_pattern)

    def add_token(self, match: Match):
        key = match.group(0)
        token = Template.Token(match.start(), match.end())

        # create the list for the key
        if key not in self._tokens:
            self._tokens[key] = []

        # append the token if it is unique
        if token not in self._tokens[key]:
            self._tokens[key].append(token)
