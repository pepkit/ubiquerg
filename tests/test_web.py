""" Tests for web """

import pytest
from ubiquerg.web import is_url


@pytest.mark.parametrize("string", ["https://www.github.com",
                                    "https://www.youtube.com"]
                         )
def test_is_url_tests_positive(string):
    assert is_url(string)


@pytest.mark.parametrize("string", ["www.github.com",
                                    "test: string spaces",
                                    "j%2vv@::https://test.com"]
                         )
def test_is_url_tests_negative(string):
    assert not is_url(string)
