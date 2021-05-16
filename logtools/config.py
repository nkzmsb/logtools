# このパッケージで取り扱うログの設定

# default.pyから移行する


# 用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]

from inspect import signature

class LogDataConfig():
    def __init__(self):
        ...
        
    def debug(self
              , message = None
              , action = None
              , function = None
              , tag = None
              , values = None
              , **args):
        ...
        
    def info(self
             , message = None
             , action = None
             , function = None
             , tag = None
             , values = None
             , **args):
        ...
        
    def _get_args(self, func):
        return set(signature(func).parameters.keys())
        
#     def _args(self):
#         print(set(signature(self.debug).parameters.keys()))