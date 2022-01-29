
from collections import namedtuple
import dataclasses
import logging
import inspect
from inspect import signature
from typing import Tuple
import warnings


##############################################
# Logのデフォルト設定
##############################################
# [ログに含める属性]
# この順番通りにログが作成される
ATTRIBUTES = tuple(["asctime", "levelname", "name", "function"
                    , "action", "exception", "message", "tag", "values"
                    ])

# 各属性のスプリッター
SPLITTER = "==="


##############################################
# 以下、コード
# ログの内容を変更したい場合には、Loggerクラスを編集する
##############################################
# logtoolsオリジナルの属性
# Loggerのdebug, info, warning, error, criticalメソッドの引数と対応している
EXTRA_ATTRIBUTES = tuple(['values', 'tag', 'function', 'exception', 'action'])

# 組み込みで用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]


@dataclasses.dataclass(frozen=True)
class LogSetting():
    # ログの設定を格納するクラス
    attributes : Tuple[str]
    splitter : str
    ExtraLogData : object
    format : str

def get_funcname(layer:int = 1)->str:
    """呼び出し元の関数名を返す
    
    呼び出し元がクラスメソッドの場合、
    "[クラス名].[メソッド名]"
    を返す。
    クラス名の取得が少し強引。もっといい方法があるかも。
    """
    
    frame = inspect.stack()[layer] # https://docs.python.org/ja/3/library/inspect.html#inspect.stack
    function_name = frame.function
    locals_dic = inspect.getargvalues(frame[0]).locals
    if ("self" in locals_dic.keys()):
        # 名前空間内にselfがある場合、呼び出し元はメソッド関数であると判断してクラス名を取りに行く
        class_name = locals_dic["self"].__class__.__name__
        return class_name + "." + function_name
    else:
        return function_name


def getLogger(name):
    return Logger(name)

class Logger():
    """
    Attributes
    ----------
    _attributes : tuple of str
        Do not change directly
    _splitter : str
        Do not change directly
    
    Notes
    -----
    For better compatibility with python standard Logger, 
    it is highly recommended to use getLogger() in this module 
    for instantiation of this class.
    """
    _attributes = ATTRIBUTES
    _splitter = SPLITTER
    
    @classmethod
    def makeformat(cls, attributes = None, splitter = None):
        """フォーマットの確認・更新を行う

        Parameters
        ----------
        attributes : tuple of str, optional
            フォーマットの属性を変更したい場合に指定, by default None
        splitter : str, optional
            フォーマットの区切り文字を変更したい場合に指定, by default None

        Returns
        -------
        LogSetting
            フォーマット情報が格納されたLogSettingインスタンス

        Raises
        ------
        ConfigurationError
            不正なフォーマット属性が指定されている場合
        """
        if attributes is None:
            attributes = cls._attributes
        if splitter is None:
            splitter = cls._splitter
        
        if not _is_attribs_available(set(attributes), set(EXTRA_ATTRIBUTES)):
            raise ConfigurationError
        
        ExtraLogData = namedtuple("ExtraLogData", EXTRA_ATTRIBUTES
                                  , defaults = [None for _ in range(len(EXTRA_ATTRIBUTES))])
        
        # make format
        ## [FutureWork]ここは関数にしてしまうべき
        form = "%(" + attributes[0] + ")s"
        if len(attributes) > 1:
            for attrib in attributes[1:]:
                form += splitter + "%(" + attrib + ")s"
                
        # クラス変数の書き換え
        cls._attributes = attributes
        cls._splitter = splitter
        
        return LogSetting(attributes=attributes, splitter = splitter
                          , ExtraLogData = ExtraLogData, format = form)
    
    def __init__(self, name=None):
        """

        Parameters
        ----------
        name : str, optional
            logger's name, by default None
            If None, the instance works only as container of configuration.
        """
        self.__name = name
        if name:
            self.__logger = logging.getLogger(name)
            self.__logger.addHandler(logging.NullHandler())
        else:
            self.__logger = None
            
        self.logsetting = Logger.makeformat()
        self._has_addStreamHandler_been_called = False
            
        
    @property
    def logger(self):
        warnings.warn(message = "logtools.Logger.logger property will be deprecated"
                      , category=PendingDeprecationWarning)
        return self.__logger
    
    @property
    def name(self):
        warnings.warn(message = "logtools.Logger.name property will be deprecated"
                      , category=PendingDeprecationWarning)
        return self.__name
        
    def trace_deco(self,func):
        """関数呼び出し前後のデバッグログ実装用デコレータ
        
        ログメッセージの内容はコンストラクタで変更可能
        """
        
        def wrap(*args,**kwargs):
            self._debug(action = "run"
                        , function = func.__qualname__
                        , tag = "trace")
                
            ret = func(*args, **kwargs)
            
            self._debug(action = "finished"
                        , function = func.__qualname__
                        , tag = "trace")
            return ret
        return wrap
        
    def _debug(self
              , message = None
              , action = None
              , function = None
              , tag = None
              , values = None):
        """debug level (for private use)

        Parameters
        ----------
        message : str, optional
        action : str, optional
        function : str, optional
            function name
            , by default None
        tag : str, optional
        values : dict, optional

        SeeAlso
        -------
        self.debug : API module
        """
        
        f = get_funcname(2) if function is None else function
        
        extralogdata = self.logsetting.ExtraLogData(action = action
                                                    , function = f
                                                    , tag = tag
                                                    , values = values)
        self._logging(extralogdata, "debug", message)
    
    def debug(self
              , message = None
              , action = None
              , tag = None
              , values = None):
        """debug level

        Parameters
        ----------
        message : str, optional
            arbitrary string
            , by default None
            
        action : str, optional
            one of the following is recommended
            - "run" : start of the processing
            - "finished" : end of the processing
            - "check" : for check
            - "ready" : the processing goes to standby
            , by default None
            
        tag : str, optional
            the following or None is recomended
            - "trace" : only for trace
            , by default None
            
        values : dict, optional
            arbitrary dictionary
            its values must be parseable
            , by default None
        """
        self._debug(message=message
                    , action=action
                    , function=get_funcname(2)
                    , tag = tag
                    , values = values)
    
    def info(self
             , message = None
             , action = None
             , tag = None
             , values = None):
        """info level

        Parameters
        ----------
        message : str, optional
            arbitrary string
            , by default None
            
        action : str, optional
            one of the following is recommended
            - "run" : start of the processing
            - "finished" : end of the processing
            - "check" : for check
            - "ready" : the processing goes to standby
            , by default None
            
        function : str, optional
            function name
            automatically completed if not specified
            , by default None
            
        tag : [type], optional
            the following or None is recomended
            - "use" : be actively used
            , by default None
            
        values : dict, optional
            arbitrary dictionary
            its values must be parseable
            , by default None
        """
        
        extralogdata = self.logsetting.ExtraLogData(action = action
                                                    , function = get_funcname(2)
                                                    , tag = tag
                                                    , values = values)
        self._logging(extralogdata, "info", message)
        
    def warning(self
                , message = None
                , exception = None
                , values = None):
        """warning level

        Parameters
        ----------
        message : str, optional
            arbitrary string
            exception message is recommended
            , by default None
            
        exception : str, optional
            exception class name
            , by default None
            
        values : dict, optional
            arbitrary dictionary
            its values must be parseable
            , by default None
        """
        
        extralogdata = self.logsetting.ExtraLogData(exception = exception
                                                    , function = get_funcname(2)
                                                    , values = values)
        self._logging(extralogdata, "warning", message)
        
    def error(self
              , message = None
              , exception = None
              , values = None):
        """error level

        Parameters
        ----------
        message : str, optional
            arbitrary string
            exception message is recommended
            , by default None
            
        exception : str, optional
            exception class name
            , by default None
            
        values : dict, optional
            arbitrary dictionary
            its values must be parseable
            , by default None
        """
        extralogdata = self.logsetting.ExtraLogData(exception = exception
                                                    , function = get_funcname(2)
                                                    , values = values)
        self._logging(extralogdata, "error", message)
        
    def critical(self
                 , message = None
                 , exception = None
                 , values = None):
        """critical level

        Parameters
        ----------
        message : str, optional
            arbitrary string
            exception message is recommended
            , by default None
            
        exception : str, optional
            exception class name
            , by default None
            
        values : dict, optional
            arbitrary dictionary
            its values must be parseable
            , by default None
        """
        extralogdata = self.logsetting.ExtraLogData(exception = exception
                                                    , function = get_funcname(2)
                                                    , values = values)
        self._logging(extralogdata, "critical", message)
    
    def setLevel(self, level):
        self.__logger.setLevel(level)
        
    def addHandler(self, hdlr):
        self.__logger.addHandler(hdlr)
    
    def add_StreamHandler(self) -> bool:
        """add StreamHandler with default format
        
        Returns
        -------
        bool
            is_added
            追加された場合にはTrue
        
        Notes
        -----
        - Jupyter等で使うときにgetLoggerした後にこれを呼び出すだけで使える
        - この処理はハンドラにStreamHandlerが１つもsetされていない場合にのみ実行される
        """

        streamhandler_exists = False
        
        for hdlr in self.__logger.handlers:
            if type(hdlr) is logging.StreamHandler:
                streamhandler_exists = True
                
        is_added = not(streamhandler_exists)
        if is_added:
            formatter = logging.Formatter(self.logsetting.format)
            hdlr = logging.StreamHandler()
            hdlr.setFormatter(formatter)
            self.addHandler(hdlr)
            
        return is_added
        
    def _logging(self, extralogdata, level, message = None):
        """ExtraLogDataの内容をロギングする

        Parameters
        ----------
        extralogdata : self._ExtraLogData
        level : str
            ログレベル
            debug, info, warning, error, critical
        message : str, optional
            message, by default None
        """
        
        extralog_dic = dict(extralogdata._asdict())
        if level == "debug":
            self.__logger.debug(msg = message
                                , extra = extralog_dic)
        elif level == "info":
            self.__logger.info(msg = message
                               , extra = extralog_dic)
        elif level == "warning":
            self.__logger.warning(msg = message
                                  , extra = extralog_dic)
        elif level == "error":
            self.__logger.error(msg = message
                                , extra = extralog_dic)
        elif level == "critical":
            self.__logger.critical(msg = message
                                   , extra = extralog_dic)
        else:
            self.__logger.warning(msg = "unexpected loglevel"
                                  , extra = extralog_dic)

def _is_attribs_available(log_attrib_set, extra_attrib_set) -> bool:
    """Logger._attributesが実現できるのかどうかを確認
    
    Parameters
    ----------
    log_attrib_set : set of str
        ログすることを所望するログ属性
    extra_attrib_set : set of str
        Loggerが準備できる組み込みではないログ属性
    
    Note
    ----------
    - extra_attrib_setにLogger._attributesに含まれない属性が含まれていたとしても
      ログ自体は正常に動作するのでTrueを返す
    Parameters
    ----------
    extra_attrib_set : set of str
        組み込みではないログ属性
    """
    # Logger._attributesが実現できるのかどうかを確認
    if not(extra_attrib_set.isdisjoint(set(ATTRIBUTE_BUILT_IN_ALL))):
        # extra_attrib_setが組み込みとかぶっていないこと
        return False
    
    # Logger._attributesの要素がすべてログ情報に含まれること
    all_attrib = extra_attrib_set | set(ATTRIBUTE_BUILT_IN_ALL)
    return log_attrib_set.issubset(all_attrib)



class ConfigurationError(Exception):
    """Logger code and ATTRIBUTES are considered inconsistent
    """
    pass







    
if __name__ == "__main__":
    import logging
    import time
    
    
    logger = Logger("AAA")
    
    logging.basicConfig(level=logging.DEBUG
                        , format=logger.logsetting.format
                        # , filename="temp/templog.log2"
                        )
    
    @logger.trace_deco
    def demofunc():
        logger.debug("in demofunc", action = "run", values = {"i" : 6})
        
    class DemoClass():
        def __init__(self):
            logger.info("@DemoClass init")
        
        @logger.trace_deco
        def demomethod(self):
            logger.warning("@DemoClass method")
    
    dc = DemoClass()
    demofunc()
    for i in range(2):
        logger.debug("aaa", action = "run", values = {"i" : i})
        logger.info("bbb", action = "finised", values = {"i" : i})
        logger.warning("ccc", values = {"val" : 5, "i" : i})
        logger.error("ddd", values = {"val" : 15, "i" : i})
        logger.critical("eee", values = {"val" : -5, "i" : i})
        time.sleep(1)
        
    dc.demomethod()
    