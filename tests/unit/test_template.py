import template_populator.template

TEST_FILE: str = '../data/test.template'


def test_template_file_is_open_negative():
    test = template_populator.template.Template()
    assert test._template_file_is_open() is False


def test_template_file_is_open_positive():
    test = template_populator.template.Template()
    test.load(TEST_FILE)
    assert test._template_file_is_open() is True
