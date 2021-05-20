
import pytest

from logtools.logging_tool import get_funcname, LoggingSetting, Logger

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
                                  , splitter = "___")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.logset
        
    def test_post_ini(self):
        assert self.logset.format == "%(A)s___%(BBB)s___%(Car)s"
        

class TestLogger():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.logger = Logger("testlogger")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.logger
        
    def test_name_prop(self):
        assert self.logger.name == "testlogger"
        
    def test_get_args(self):
        expect_debug = set(["message", "action", "function", "tag", "values"])
        assert self.logger._get_args(self.logger.debug) == expect_debug
        
    def test_get_all_attributes(self):
        attribs_ls = ["message", "action", "function", "tag", "values", "expection"]
        expect = LoggingSetting(attributes = attribs_ls, splitter = "___")
        assert self.logger._get_all_attributes() == expect