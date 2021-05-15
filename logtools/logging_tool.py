
import logging
import inspect

class Logger():
    def __init__(self):
        ...
        
    def logger(self):
        # return logging.Loggerインスタンス
        ...
        
    def log_deco(self):
        # トレース用ログ自動作成デコレータ
        ...
        
    def debug(self):
        ...
        
    def info(self):
        ...
        
    def warning(self):
        ...
        
    def error(self):
        ...
        
    def critical(self):
        ...
   
        
def get_funcname(layer:int = 0)->str:
    """呼び出し元の関数名を返す
    
    呼び出し元がクラスメソッドの場合、
    "[クラス名].[メソッド名]"
    を返す。
    クラス名の取得が少し強引。もっといい方法があるかも。
    """
    
    frame = inspect.stack()[1] # https://docs.python.org/ja/3/library/inspect.html#inspect.stack
    function_name = frame.function
    locals_dic = inspect.getargvalues(frame[layer]).locals
    if ("self" in locals_dic.keys()):
        # 名前空間内にselfがある場合、呼び出し元はメソッド関数であると判断してクラス名を取りに行く
        class_name = locals_dic["self"].__class__.__name__
        return class_name + "." + function_name
    else:
        return function_name
    
    
if __name__ == "__main__":
    class CallingClass():
        def __init__(self):
            self.in_init = get_funcname()
            
        def calling_method(self):
            aaa = get_funcname()
            print(aaa)
            return get_funcname()
        
    cc = CallingClass()
    print(cc.calling_method())