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


def test_file_is_open_negative(resource: src.template.Template):
    assert resource._file_is_open() is False


def test_file_is_open_positive(resource: src.template.Template):
    resource.load(TEST_FILE)
    assert resource._file_is_open() is True
