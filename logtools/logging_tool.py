
from collections import namedtuple
import dataclasses
import logging
import inspect
from inspect import signature
from typing import Tuple


##############################################
# LogのSetting
##############################################
# [ログに含める属性]
# この順番通りにログが作成される
ATTRIBUTES = tuple(["asctime", "levelname", "name", "function"
                    , "action", "exception", "message", "tag", "values"
                    ])

# 各属性のスプリッター
SPLITTER = "___"


##############################################
# 以下、コード
# ログの内容を変更したい場合には、Loggerクラスを編集する
##############################################


# 組み込みで用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]


@dataclasses.dataclass
class LoggingSetting():
    # ログの設定を格納するクラス
    attributes : Tuple[str]
    splitter : str
    
    def __post_init__(self):
        # make format
        form = "%(" + self.attributes[0] + ")s"
        if len(self.attributes) > 1:
            for attrib in self.attributes[1:]:
                form += self.splitter + "%(" + attrib + ")s"
                
        self.format = form


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


class Logger():
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
        
        self.extra_attribs = self._get_extra_attribs()    
        self.logsetting = self._make_loggingsetting()
        
        # extra引数でログする内容のコンテナ
        self._ExtraLogData = namedtuple("ExtraLogData", self.extra_attribs
                                        , defaults = [None for _ in range(len(self.extra_attribs))])
            
        
    @property
    def logger(self):
        return self.__logger
    
    @property
    def name(self):
        return self.__name
        
    def log_deco(self):
        # トレース用ログ自動作成デコレータ
        ...
        
    def debug(self
              , message = None
              , action = None
              , function = None
              , tag = None
              , values = None):
        
        extralogdata = self._ExtraLogData(action = action
                                          , function = get_funcname(2)
                                          , tag = tag
                                          , values = values)
        self._logging(extralogdata, "debug", message)
        
    def info(self
             , message = None
             , action = None
             , function = None
             , tag = None
             , values = None):
        ...
        
    def warning(self
                , message = None
                , exception = None
                , function = None
                , values = None):
        ...
        
    def error(self
              , message = None
              , exception = None
              , function = None
              , values = None):
        ...
        
    def critical(self
                 , message = None
                 , exception = None
                 , function = None
                 , values = None):
        ...
        
    def _get_args(self, func) -> set:
        # メソッド（関数）のパラメータを取得する
        return set(signature(func).parameters.keys())
    
    def _get_extra_attribs(self) -> set:
        """組み込みではないログ属性のsetを取得する
        
        ログメソッドのパラメータを重複なく取得する
        """
        attrib_set = self._get_args(self.debug)
        attrib_set = attrib_set | self._get_args(self.info)
        attrib_set = attrib_set | self._get_args(self.warning)
        attrib_set = attrib_set | self._get_args(self.error)
        attrib_set = attrib_set | self._get_args(self.critical)
        
        return attrib_set - set(["message"]) # messageは組み込み属性
    
    def _is_attribs_available(self, extra_attrib_set) -> bool:
        """ATTRIBUTESが実現できるのかどうかを確認
        
        Note
        ----------
        - extra_attrib_setにATTRIBUTESに含まれない属性が含まれていたとしても
          ログ自体は正常に動作するのでTrueを返す

        Parameters
        ----------
        extra_attrib_set : set of str
            組み込みではないログ属性
        """
        # ATTRIBUTESが実現できるのかどうかを確認
        if not(extra_attrib_set.isdisjoint(set(ATTRIBUTE_BUILT_IN_ALL))):
            # extra_attrib_setが組み込みとかぶっていないこと
            return False
        
        # ATTRIBUTESの要素がすべてログ情報に含まれること
        all_attrib = extra_attrib_set | set(ATTRIBUTE_BUILT_IN_ALL)
        return set(ATTRIBUTES).issubset(all_attrib)
    
    def _make_loggingsetting(self) -> LoggingSetting:
        if self._is_attribs_available(self.extra_attribs):
            return LoggingSetting(ATTRIBUTES, SPLITTER)
        else:
            raise ConfigurationError
        
        
        
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
        

class ConfigurationError(Exception):
    """Logger code and ATTRIBUTES are considered inconsistent
    """
    pass
    
if __name__ == "__main__":
    import logging
    
    
    aaa = Logger("AAA")
    
    # f = logging.Formatter(aaa.logsetting.format)
    logging.basicConfig(level=logging.DEBUG, format=aaa.logsetting.format)
    
    aaa.debug("aaa", action = "run")
    