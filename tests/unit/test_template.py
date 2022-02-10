import pathlib
import sys

# fix for pytest discovery (this is the worst thing *ever*)
# this is used to work with VS Code's built in pytest tools
root_dir: str = str(pathlib.Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    print('added to PATH')
    sys.path.append(root_dir)

import pytest
import src.template

TEST_FILE: str = 'tests/data/test.template'
TEST_EXPECTED_FILE: str = 'tests/data/test_expected.template'


@pytest.fixture()
def resource():
    # setup test
    test = src.template.Template()

    # perform test
    yield test

    # teardown test
    return

# ensure the the file opened through Template.load()
# is the same as a file we open manually
def test_load(resource: src.template.Template):
    import os
    with open(TEST_FILE, 'r') as file:
        expected_stat = os.fstat(file.fileno())
        resource.load(TEST_FILE)
        test_stat = os.fstat(resource._file.fileno())
        assert test_stat == expected_stat

# ensure that Template.scan() takes the loaded file,
# scans it for tokens encapsulated with ${}, and adds
# the tokens to it's internal map of tokens.
def test_scan(resource: src.template.Template):
    resource.load(TEST_FILE)
    resource.scan()

    assert "${Namespace}" in resource._tokens
    assert resource._tokens["${Namespace}"] == ''
    assert "${ClassName}" in resource._tokens
    assert resource._tokens["${ClassName}"] == ''

# ensure the Template.replace modified each token's
# replacement attribute
@pytest.mark.parametrize(
    "key,replacement", [
        ('${Namespace}', 'test_namespace'),
        ('${ClassName}', 'TestClass')
])
def test_replace(resource: src.template.Template, key: str, replacement: str):
    resource.load(TEST_FILE)
    resource.scan()
    resource.replace(key, replacement)

    for token in resource._tokens[key]:
        assert token.replacement == replacement
