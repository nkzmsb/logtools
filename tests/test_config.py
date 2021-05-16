

import pytest

from logtools.config import _get_params


def test_get_params():
    def dummy(a, b, c = 0):
        ...    
    expect = set(["a", "b", "c"])
    assert _get_params(dummy) == expect
    
    def dummy2(a, b, *args, c = 0, **kwargs):
        ...    
    expect2 = set(["a", "b", "c"])
    assert _get_params(dummy2) == expect2