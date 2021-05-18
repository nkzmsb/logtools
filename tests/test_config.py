

import pytest

from logtools.config import _get_params, _get_getargvalues


def test_get_params():
    def dummy(a, b, c = 0):
        ...    
    expect = set(["a", "b", "c"])
    assert _get_params(dummy) == expect
    
    def dummy2(a, b, *args, c = 0, **kwargs):
        ...    
    expect2 = set(["a", "b", "c"])
    assert _get_params(dummy2) == expect2
    
def test_get_getargvalues():
    def dummy(a, b, c = 0):
        return _get_getargvalues()
    expect = {"a":[1,2,3], "b":"BBB", "c":3}
    assert dummy([1,2,3], "BBB", 3) == expect