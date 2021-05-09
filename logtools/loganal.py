
import ast
import warnings


def keymake(k, head_str = None):
    if head_str:
        return head_str + "-" + k
    else:
        return k


def expand_dict(dic, head_str = None):
    # dictの内容を展開する
    
    expanded_dic = {}
    remain_dic = {}
    for k,v in dic.items():
        if type(v) == dict:
            remain_dic[keymake(k, head_str)] = v
        else:
            expanded_dic[keymake(k, head_str)] = v
            
    return expanded_dic, remain_dic


def breakdown_values(values):
    
    try:
        values_lit = ast.literal_eval(values)
    except SyntaxError:
        warnings.warn("values is not valid")
        return {"values" : values, "values_breakdown_error" : "Error"}
    
    if type(values)==dict:
        res_dic = {"AAA" : "AAA"}
    else:
        # Only dict is valid as type of values_lit
        # but some other type also works. 
        warnings.warn("values is not valid but work")
        res_dic = {"values" : values_lit, "values_breakdown_error" : "Warning"}
    
    return res_dic


def log_to_dict(unitlog_str)->dict:
    # values以外をdict化
    # valuesをbreakdown_values()で分解
    # valuesの内容をdictに追加
    return {"aa":0}

def logfile_converter(filepath)->"list of dict":
    # log_to_dict()をループ
    ...
    
def renamefiles(dirpath):
    # フォルダ内の**.log#を**_#.logに変換
    # 変換後のファイル名のリストをreturn
    ...


class LogData():
    def __init__(self):
        # renamefiles()
        # logfile_converterのループ
        # self.log_dfの作成
        ...
        
    @property
    def log_df(self):
        # self.log_dfのコピーを返す
        ...
        
    # [FutureWork]
    # def export_db(self):
    #     ...