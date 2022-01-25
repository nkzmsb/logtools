
import logging
from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC

import pytest
# from testfixtures import LogCapture

from logtools.logging_tool import get_funcname, LoggingSetting, getLogger
from logtools.logging_tool import _get_args

def test_get_funcname_at_func():
    def callingfunc():
        return get_funcname()
    
    assert callingfunc() == "callingfunc"
    
def test_get_funcname_at_class():
    class CallingClass():
        def __init__(self):
            self.in_init = get_funcname()
            
        def calling_method(self):
            return get_funcname()
        
    cc = CallingClass()
    
    assert cc.in_init == "CallingClass.__init__"
    assert cc.calling_method() == "CallingClass.calling_method"
    
class TestLoggingSetting():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.logset = LoggingSetting(attributes=["A", "BBB", "Car"]
                                  , splitter = "===")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.logset
        
    def test_post_ini(self):
        assert self.logset.format == "%(A)s===%(BBB)s===%(Car)s"
        

class TestLogger():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.logger = getLogger("testlogger")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.logger
        
    def test_name_prop(self):
        assert self.logger.name == "testlogger"
    
    def test_get_extra_attribs(self):
        expect = set(['values', 'tag', 'function', 'exception', 'action'])
        assert self.logger._get_extra_attribs() == expect
    
    @pytest.mark.parametrize("attrib, expect"
                             , [(['values', 'tag', 'function', 'exception', 'action']
                                 , True)
                                , (['values', 'tag', 'function', 'exception']
                                   , False) # 不足
                                , (['values', 'tag', 'function', 'foo', 'exception', 'action']
                                   , True) # 過剰は問題ない
                                ])
    def test_is_attribs_available(self, attrib, expect):
        assert self.logger._is_attribs_available(set(attrib)) == expect
        
    def test_make_loggingsetting(self):
        attribs_tpl = tuple(["asctime", "levelname", "name", "function"
                             , "action", "exception", "message", "tag", "values"
                             ])
        expect = LoggingSetting(attributes = attribs_tpl, splitter = "===")
        assert self.logger._make_loggingsetting() == expect
        
        
    def test_ExtraLogData(self):
        eld = self.logger._ExtraLogData()
        
        expect = {key : None for key in ["action", "values", "exception", "function", "tag"]}
        assert dict(eld._asdict()) == expect
    
    def test_add_StreamHandler(self):
        self.logger.add_StreamHandler()
        added_handler=self.logger._Logger__logger.handlers[-1] # __loggerにアクセスするためには、_Logger__loggerとする必要がある
        
        assert isinstance(added_handler, logging.StreamHandler)
        
        assert added_handler.formatter._fmt == "%(asctime)s===%(levelname)s===%(name)s===%(function)s===%(action)s===%(exception)s===%(message)s===%(tag)s===%(values)s"
    
    @pytest.mark.skip(reason="ログのテストの仕方を要確認")
    def test_logging(self, capture):
        ...
    
def test_get_args():
    def target(message, action, tag="aaa", values=False):
        return None
    expect = set(["message", "action", "tag", "values"])
    assert _get_args(target) == expect
    
    class Bar():
        def __init__(self, foo):
            self.foo = foo
        def target(self, message, action, tag="aaa", values=False):
            return None
    bar = Bar("foo")
    assert _get_args(bar.target) == expect