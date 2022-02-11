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
        self._tokens = {}
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
        self._file.seek(0)

    def replace(self, key: str, replacement: str) -> None:
        if key in self._tokens.keys():
            self._tokens[key] = replacement

    def render(self) -> io.StringIO:
        rendered: io.StringIO = io.StringIO()

        self._file.seek(0)
        for line in self._file:
            tmp: str = line

            for key in self._tokens.keys():
                tmp = tmp.replace(key, self._tokens[key])

            rendered.write(tmp)

        self._file.seek(0)
        rendered.seek(0)
        return rendered
    
    def export(self, path: str):
        with open(path, 'w') as file:
            rendered = self.render()
            file.write(rendered.read())

    def get_keys(self):
        return self._tokens.keys()

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


if __name__ == '__main__':
    resource = Template()
    
    resource.load(input('load template file (absolute path): '))
    
    print('scanning...')
    resource.scan()

    print('provide replacement: ')
    for key in resource.get_keys():
        resource.replace(key, input(f'replace {key} with: '))

    resource.export(input('export to (absolute path (incl. filename and ext): '))
    print('finished')