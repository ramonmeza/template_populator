from collections import namedtuple
from typing import Dict, Iterator, List, Match

import io
import re


class Template:

    # token contains it's start and end positions in the file
    Token = namedtuple("Token", "line_num start end")
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

        line_num: int = 0
        for line in self._file:
            # increment line number
            line_num += 1

            # get the token
            tokens = Template._scan_line(self._token_pattern, line)

            # add each token
            for token in tokens:
                self._add_token(line_num, token)

    def _scan_line(token_pattern: str, line: str) -> Iterator[Match]:
        return re.finditer(token_pattern, line)

    def _add_token(self, line_num: int, match: Match):
        key = match.group(0)
        token = Template.Token(line_num, match.start(), match.end())

        # create the list for the key
        if key not in self._tokens:
            self._tokens[key] = []

        # append the token if it is unique
        if token not in self._tokens[key]:
            self._tokens[key].append(token)
