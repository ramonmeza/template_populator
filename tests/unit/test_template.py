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


@pytest.fixture()
def resource():
    # setup test
    test = src.template.Template()

    # perform test
    yield test

    # teardown test
    return


def test_load(resource: src.template.Template):
    import os
    with open(TEST_FILE, 'r') as file:
        expected_stat = os.fstat(file.fileno())

        resource.load(TEST_FILE)
        test_stat = os.fstat(resource._file.fileno())

        assert test_stat == expected_stat


def test_scan(resource: src.template.Template):
    resource.load(TEST_FILE)
    resource.scan()
    assert "${Namespace}" in resource._tokens
    assert "${ClassName}" in resource._tokens
    assert len(resource._tokens["${Namespace}"]) == 5
    assert len(resource._tokens["${ClassName}"]) == 8
