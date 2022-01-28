from collections import namedtuple
import dataclasses
import logging
from ssl import ALERT_DESCRIPTION_BAD_RECORD_MAC
from attr import attributes

import pytest
# from testfixtures import LogCapture

from logtools.logging_tool import get_funcname, LogSetting, getLogger, Logger, ConfigurationError
from logtools.logging_tool import _is_attribs_available

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
    
class TestLogSetting():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.logset = LogSetting(attributes=["A", "BBB", "Car"]
                                 , splitter = "==="
                                 , ExtraLogData = namedtuple("ExtraLogData", ["a"])
                                 , format = "%(A)s===%(BBB)s===%(Car)s")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.logset
        
    def test_frozen(self):
        with pytest.raises(dataclasses.FrozenInstanceError):
            self.logset.splitter = "---"
        
    def test_ini(self):
        extralogdata = self.logset.ExtraLogData(a = 3)
        assert extralogdata._asdict() == {"a":3}

class TestLogger():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.logger = getLogger("testlogger")

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        
        # logging.Loggerは名前によってグローバルに情報共有されているため、
        # logtools.Loggerインスタンスやlogtools.Logger.__loggerを削除しても
        # メモリ上に残り続ける
        # ハンドラのテストのコンタミをなくすためにはLoggerの名前を変更するか、
        # ハンドラを強制的に初期化するか。今回は後者を選択した。
        self.logger._Logger__logger.handlers = []
        del self.logger
        
    def test_name_prop(self):
        assert self.logger.name == "testlogger"        
        
    def test_ExtraLogData(self):
        eld = self.logger.logsetting.ExtraLogData()
        
        expect = {key : None for key in ["action", "values", "exception", "function", "tag"]}
        assert dict(eld._asdict()) == expect
    
    def test_add_StreamHandler(self):
        self.logger.add_StreamHandler()
        added_handler=self.logger._Logger__logger.handlers[-1] # __loggerにアクセスするためには、_Logger__loggerとする必要がある
        
        assert isinstance(added_handler, logging.StreamHandler)
        
        assert added_handler.formatter._fmt == "%(asctime)s===%(levelname)s===%(name)s===%(function)s===%(action)s===%(exception)s===%(message)s===%(tag)s===%(values)s"
    
    def test_add_StreamHandler_manytime(self):
        """add_StreamHandlerはLoggerに1つもStreamHandlerが存在しない場合にのみ実行される"""
        
        assert self.logger.add_StreamHandler()
        for _ in range(3):
            assert not(self.logger.add_StreamHandler())

    @pytest.mark.skip(reason="ログのテストの仕方を要確認")
    def test_logging(self, capture):
        ...

class TestLoggerClassMethod_and_Val():
    """Loggerのクラスメソッド・クラス変数のテスト
    
    Notes
    -----
    - クラスメソッドやクラス変数をいじると、他のテストに影響するので遮蔽
    - [FutureWork]テストが失敗するとteardownが呼ばれないので、遮蔽できない。改善必要。
    """
    def setup_method(self,method):
        print('run : method={}'.format(method.__name__))

    def teardown_method(self, method):
        # 元に戻す：これもmakeformatメソッドが正しく動作しておく必要がある
        Logger.makeformat(attributes = tuple(["asctime", "levelname", "name", "function"
                                              , "action", "exception", "message", "tag", "values"
                                              ])
                          , splitter = "===")
        print('finished : method={}'.format(method.__name__))
        
    def test_makeformat_default(self):
        """Loggerクラスメソッドのtest_makeformat()のテスト"""
        expect = LogSetting(attributes=tuple(["asctime", "levelname", "name", "function", "action", "exception", "message", "tag", "values"])
                            , splitter = "==="
                            , format = "%(asctime)s===%(levelname)s===%(name)s===%(function)s===%(action)s===%(exception)s===%(message)s===%(tag)s===%(values)s"
                            , ExtraLogData = namedtuple("ExtraLogData", set(['values', 'tag', 'function', 'exception', 'action']))
                            )
        logsetting = Logger.makeformat()
        assert logsetting.attributes == tuple(["asctime", "levelname", "name", "function", "action", "exception", "message", "tag", "values"])
        assert logsetting.splitter == "==="
        assert logsetting.format == "%(asctime)s===%(levelname)s===%(name)s===%(function)s===%(action)s===%(exception)s===%(message)s===%(tag)s===%(values)s"
        extralogdata = logsetting.ExtraLogData()
        expect = {key:None for key in ['values', 'tag', 'function', 'exception', 'action']}
        assert extralogdata._asdict() == expect
    
    def test_makeformat_nondefault(self):
        """Loggerクラスメソッドのtest_makeformat()のテスト:引数指定"""
        expect = LogSetting(attributes=tuple(["asctime", "function", "message"])
                            , splitter = "~~~"
                            , format = "%(asctime)s~~~%(function)s~~~%(message)s"
                            , ExtraLogData = namedtuple("ExtraLogData", set(['function']))
                            )
        logsetting = Logger.makeformat(attributes=tuple(["asctime", "function", "message"])
                                       , splitter = "~~~")
        assert logsetting.attributes == tuple(["asctime", "function", "message"])
        assert logsetting.splitter == "~~~"
        assert logsetting.format == "%(asctime)s~~~%(function)s~~~%(message)s"
        # Note : ExtraLogDataはmakeformatの引数が与えられても変化しない
        extralogdata = logsetting.ExtraLogData()
        expect = {key:None for key in ['values', 'tag', 'function', 'exception', 'action']}
        assert dict(extralogdata._asdict()) == expect
        assert Logger._attributes == tuple(["asctime", "function", "message"])
        assert Logger._splitter == "~~~"
        
    def test_makeformat_raise(self):
        with pytest.raises(ConfigurationError):
            Logger.makeformat(attributes = tuple(["action", "foo"]))
            
    def test_Logger_class_variable(self):
        assert Logger._attributes == tuple(["asctime", "levelname", "name", "function"
                                            , "action", "exception", "message", "tag", "values"])
        assert Logger._splitter == "==="
    
@pytest.mark.parametrize("attrib, expect"
                         , [(['values', 'tag', 'function', 'exception', 'action'], True)
                            , (['values', 'tag', 'function', 'exception'], False) # 不足
                            , (['values', 'tag', 'function', 'foo', 'exception', 'action'], True) # 過剰は問題ない
                            ])
def test_is_attribs_available(attrib, expect):
    assert _is_attribs_available(set(["asctime", "levelname", "name", "function"
                                      , "action", "exception", "message", "tag", "values"
                                      ]),set(attrib)) == expect
    