from ast import arg
import io
import re

class Template:

    TOKEN_REGEX_PATTERN: str = '\$\{([a-zA-Z_]*):?([a-zA-Z_]*)\}'

    _file: io.TextIOWrapper
    _tokens: dict

    def __init__(self) -> None:
        self._file = None
        self._tokens = {}

    def __del__(self) -> None:
        # close the file if it's loaded and open
        if self.is_loaded():
            self._file.close()

    def load(self, path: str) -> bool:
        try:
            self._file = open(path, 'r')
            self._scan()
            return True

        except Exception as e:
            print(repr(e))

        return False

    def _scan(self) -> None:
        if not self.is_loaded():
            return
        
        self._file.seek(0)
        for line in self._file:
            matches = re.finditer(Template.TOKEN_REGEX_PATTERN, line)

            # add each token with an empty replacement
            for match in matches:
                key = match.group(1)
                self._tokens[key] = ''

        self._file.seek(0)
    
    def render(self) -> io.StringIO:
        if not self.is_loaded():
            return None

        self._file.seek(0)
        rendered = io.StringIO()
        for line in self._file:
            rendered_line = line

            matches = re.finditer(Template.TOKEN_REGEX_PATTERN, rendered_line)

            for match in matches:
                replace_me: str = match.group(0)
                key: str = match.group(1)
                replacement: str = self._tokens[key]

                try:
                    modifier: str = getattr(replacement, match.group(2))
                    replacement = modifier()
                except Exception as e:
                    pass

                rendered_line = rendered_line.replace(replace_me, replacement)

            rendered.write(rendered_line)
        
        self._file.seek(0)
        rendered.seek(0)

        return rendered
    
    def replace(self, key: str, replacement: str) -> bool:
        if key in self._tokens.keys():
            self._tokens[key] = replacement
            return True

        print(f'Key not found in template: {key}')
        return False

    def is_loaded(self):
        # if the file isn't loaded
        if not self._file or self._file.closed:
            print('No template loaded!')
            return False

        return True

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--template_file',
        dest='template_file',
        required=False,
        help='path to the template file')
    parser.add_argument(
        '-o',
        '--output',
        dest='output_file',
        required=False,
        help='path to the output file')
    parser.add_argument(
        '-r',
        '--replace',
        dest='replacements',
        action='append',
        nargs='+',
        required=False,
        help='replace a token in your template, ' +
             'use format: -r key:value_to_replace_with')
    args = parser.parse_args()

    template = Template()
    template.load(args.template_file)

    for replacement in args.replacements:
        key, value = map(str, replacement[0].split(':'))
        template.replace(key, value)
    
    with open(args.output_file, 'w+') as file:
        file.write(template.render().getvalue())