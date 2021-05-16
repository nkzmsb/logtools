# このパッケージで取り扱うログの設定

# default.pyから移行する


# 用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]

from inspect import signature

def _get_params(func) -> set:
    """関数のパラメータを取得する
    """
    args_set = set(signature(func).parameters.keys())
    
    return args_set - set(["args", "kwargs"])

class LogDataConfig():
    """ロギングの設定
    
    - ここでは設定部分のみが定義される
    - ロギング用クラスにはこのクラスを継承させることで、ロギングに設定を反映する
    - 解析用モジュールには、そこでインスタンス化することで設定を反映する
    """ 
    
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