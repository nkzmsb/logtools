
import dataclasses
import logging
import inspect
from inspect import signature
from typing import Awaitable


##############################################
# LogのSetting
##############################################
# [ログに含める属性]
# この順番通りにログが作成される
ATTRIBUTES = tuple(["asctime", "levelname", "name", "func"
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
    attributes : list[str]
    splitter : str
    
    def __post_init(self):
        # make format
        self.fomat = ...


# [Issue]ATTRIBUTE_EXTRAはLoggerクラス内で作られるので、
# このクラス定義もLoggerクラス内に持っていく必要があるけど、どうやって？？
# [FutureWork]
# make_dataclassは動的にdataclassを作れるため便利だが
# テストがしにくいし、あまりいい方法ではない。
# 改善が望まれる。
# 型がanyになっているのも、実害はないが好ましい状態ではない。
ExtraLogData = dataclasses.make_dataclass(cls_name = "ExtraLogData"
                                          , fields = [(attr, any, None) for attr in ATTRIBUTE_EXTRA])


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
            
        self.logsetting = self._get_all_attributes()
            
        
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
        ...
        # logdata = ExtraLogData()
        # self._logging(logdata, level, message)
        
    def info(self
             , message = None
             , action = None
             , function = None
             , tag = None
             , values = None):
        ...
        
    def warning(self
                , message = None
                , action = None
                , function = None
                , tag = None
                , values = None):
        ...
        
    def error(self):
        ...
        
    def critical(self):
        ...
        
    def _get_args(self, func):
        # メソッド（関数）のパラメータを取得する
        return set(signature(func).parameters.keys())
    
    def _get_all_attributes(self) -> LoggingSetting:
        # - ログメソッドのパラメータを重複なく取得する->extra attribute
        # - LoggingSettingを作成する
        #   - formatが実現できるのかどうかを確認
        ...
        
    def _logging(self, extralogdata, level, message = None):
        # ExtraLogDataの内容をロギングする
        # どうやってレベル指定する？->気合で手動が現在有力
        ...
        # if level == "debug":
        #     self.__logger.debug(msg = message
        #                         , extra=dataclasses.asdict(extralogdata))
        # elif level == "info":
        #     self.__logger.info(msg = message
        #                        , extra=dataclasses.asdict(extralogdata))
        # elif ...
   
        


    
if __name__ == "__main__":
    def deco(f):
        def wrapper():
            print("in wrapper:",f.__name__)
            return f()
        return wrapper
        
    @deco
    def callingfunc():
        return get_funcname()
    
    print(LogData())