

import pytest

from logtools.config import _get_params, _get_getargvalues,LogDataConfig


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
    
    
class TestLogDataConfig():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.ldc = LogDataConfig()

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.ldc
        
    def test_get_args(self):
        # このテストはLogDataConfigの引数仕様を変更すると失敗する
        expect = set(["message", "action", "function", "tag", "values"]) 
        assert self.ldc._get_args(self.ldc.debug) == expect