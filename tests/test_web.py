""" Tests for web """

import pytest
from ubiquerg.web import is_url


@pytest.mark.parametrize("s", ["https://www.github.com",
                                    "https://www.youtube.com"]
                         )
def test_is_url_tests_positive(s):
    assert is_url(s)


@pytest.mark.parametrize("s", ["www.github.com",
                                    "test: string spaces",
                                    "j%2vv@::https://test.com"]
                         )
def test_is_url_tests_negative(s):
    assert not is_url(s)
