
import pytest

from logtools.logging_tool import get_funcname

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
    assert cc.calling_method == "CallingClass.calling_method"