import os
import pathlib
import sys

# fix for pytest discovery (this is the worst thing *ever*)
# this is used to work with VS Code's built in pytest tools
root_dir: str = str(pathlib.Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    print('added to PATH')
    sys.path.append(root_dir)

import pytest
from src.template import Template

TEST_FILE: str = 'tests/data/test.template'
TEST_EXPECTED_FILE: str = 'tests/data/test_expected.template'


@pytest.fixture()
def resource():
    # setup test
    test = Template()

    # perform test
    yield test

    # teardown test
    return

def test_load(resource: Template):
    with open(TEST_FILE, 'r') as file:
        resource.load(TEST_FILE)
        assert resource._file.read() == file.read()

    assert 'test_case_name' in resource._tokens
    assert resource._tokens['test_case_name'] == ''
    assert 'test_key' in resource._tokens
    assert resource._tokens['test_key'] == ''

@pytest.mark.parametrize(
    'key,replacement', [
        ('test_case_name', 'A'),
        ('test_key', 'kEy')
])
def test_replace(resource: Template, key: str, replacement: str):
    resource.load(TEST_FILE)
    resource.replace(key, replacement)

    assert resource._tokens[key] == replacement

# ensure that TemplateApi.render() produces the same
# output as our expected test TemplateApi file when read
def test_render(resource: Template):
    resource.load(TEST_FILE)
    
    resource.replace('test_case_name', 'A')
    resource.replace('test_key', 'kEy')

    with open(TEST_EXPECTED_FILE, 'r') as file:
        result = resource.render()
        assert result.read() == file.read()