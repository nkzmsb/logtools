# このパッケージで取り扱うログの設定

# default.pyから移行する


# 用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]

import inspect
from inspect import signature

# いらない気がする。。
def _get_params(func) -> set:
    """関数のパラメータを取得する
    """
    args_set = set(signature(func).parameters.keys())
    
    return args_set - set(["args", "kwargs"])

# これもいらない気がする。。
def _get_getargvalues():
    parent_frame = inspect.currentframe().f_back
    info = inspect.getargvalues(parent_frame)
    return {key: info.locals[key] for key in info.args}

class LogDataConfig():
    """ロギングの設定
    
    - ここでは設定部分のみが定義される
    - ロギング用クラスにはこのクラスを継承させることで、ロギングに設定を反映する
    - 解析用モジュールには、そこでインスタンス化することで設定を反映する
    """
    
    #[ToDo] kwargsとかいらない。
    # この形式にのっとりたくなければ、普通にログ取ればいい
    
    def __init__(self):
        ...
        
    def debug(self
              , message = None
              , action = None
              , function = None
              , tag = None
              , values = None):
        ...
        
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
        
    def _get_args(self, func):
        return set(signature(func).parameters.keys())
    
    def _get_all_attributes(self):
        ...
        
#     def _args(self):
#         print(set(signature(self.debug).parameters.keys()))