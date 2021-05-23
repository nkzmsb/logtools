
from __future__ import annotations # python3.9以降では不要

import ast
import copy
import glob
import os
import re
import warnings


import pandas as pd

# from logtools.default import default
from logtools.logging_tool import Logger

logger = Logger()

ATTRIBUTES = logger.logsetting.attributes
FORMATTER = logger.logsetting.format
SPLITTER = logger.logsetting.splitter

def keymake(k_str, head_str = None):
    if head_str:
        return head_str + "-" + k_str
    else:
        return k_str


def expand_dict(dic, head_str = None):
    """dicの内容を展開する
    
    dicのネストを一段階展開する
    実際の動作はネストされている辞書をremain_dicにまとめる

    Parameters
    ----------
    dic : dict
        展開する辞書
    head_str : str, optional
        展開後の辞書のヘッダー, by default None

    Returns
    -------
    expanded_dic : dict
        ネストされていない辞書
    remain_dic : dict
        ネストされていた辞書
    """
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
    """辞書のログ内容（文字列）を展開された辞書型に変換する
    
    辞書のネストはすべて展開される

    Parameters
    ----------
    values : str
        ast.literal_eval(values)で辞書型が返る文字列

    Returns
    -------
    dict
        展開された辞書
        
    Warnings
    -------
    UserWarning(values is not valid)
        valuesが辞書型に変換することができず、文字列としか認識できない場合
        返値の辞書には"values"キーに引数の文字列がそのまま、
        "convert_exception"キーに"values error"が入る
    
    UserWarning(values is not valid but work)
        valuesが辞書型に変換することができないが、そのほかの型として認識できる場合
        返値の辞書には"values"キーに評価された引数の値が、
        "convert_exception"キーに"values warning"が入る
    """
    
    try:
        values_lit = ast.literal_eval(values)
    except SyntaxError:
        warnings.warn("values is not valid")
        return {"values" : values, "convert_exception" : "values error"}
    
    if type(values_lit)==dict:
        
        expanded_dic, remain_dic = expand_dict(values_lit)
        
        while True:
            try:
                k,v = remain_dic.popitem()
            except KeyError:
                # remain_dic is empty
                break
            
            new_exp_dic, still_rem_dic = expand_dict(v, k)
            
            expanded_dic.update(new_exp_dic)
            remain_dic.update(still_rem_dic)
        
        res_dic = expanded_dic
        
    else:
        # Only dict is valid as type of values_lit
        # but some other type also works. 
        warnings.warn("values is not valid but work")
        res_dic = {"values" : values_lit, "convert_exception" : "values warning"}
    
    return res_dic


def log_to_dict(unitlog_str, attributes_tpl = ATTRIBUTES, splitter_str = SPLITTER)->dict:
    """log文字列を辞書に変換する

    Parameters
    ----------
    unitlog_str : str
        1つのログ
    attributes_tpl : tpl of str, optional
        ログの項目, by default ATTRIBUTES
    splitter_str : str, optional
        ログの各項目の仕切り文字, by default SPLITTER

    Returns
    -------
    dict
        辞書化されたログ
    """
    
    # ログを成分に分解する
    # splitの引数に最大分割回数を設定することもできるが、
    # フォーマット異常検知のためにそれは行わない
    log_ls = unitlog_str.split(splitter_str)
    
    # [FutureWork] 要検討
    # フォーマット異常を検知する方法がlog_lsの長さを見るしかない
    # これが限界な気もするが...
    if len(log_ls) != len(attributes_tpl):
        # warning
        warnings.warn("strange format")
        return {"values" : unitlog_str, "convert_exception" : "strange format"}
    
    ret_dic = {}
    for k,v in zip(attributes_tpl[:-1], log_ls[:-1]):
        try:
            # 可能なものは型評価
            v_lit = ast.literal_eval(v)
        except (SyntaxError, ValueError):
            v_lit = v
        ret_dic[k] = v_lit
    
    # values属性の処理
    val_dic = breakdown_values(log_ls[-1])
    ret_dic.update(val_dic)
    
    return ret_dic

def logfile_converter(filepath)->list[dict]:
    # log_to_dict()をループ

    with open(filepath,"r") as f:
        log_ls = []
        for line in f:
            log_ls.append(log_to_dict(line.replace("\n", "")))
    
    return log_ls
    
def newlogfilename(prename, base):
    match = re.search(r'\.log.+', prename)
    if match:
        num = match.group()[4:]
    else:
        num = "1"
    
    return base + "_" + num + ".log"
        

def renamefiles(dirpath, base):
    """RotatingFileHandlerで作成されたlogファイル名を修正する
    
    dirpathディレクトリ内の"*.log#"という名前のファイルを
    "[base]_#.log"という名前に変更する。
    *は任意の文字列、#は番号（任意の文字列でも動作）

    Parameters
    ----------
    dirpath : path
        logファイルが収められているディレクトリのパス
    base : str
        修正後ファイルの名前のベース部分

    Returns
    -------
    list of path
        修正後のファイルパスのリスト
        
    # [FutureWork]
    # - ディレクトリにややこしい名前のファイルも存在する場合に対応する
    # - 2回以上実行すると変なファイル名になってしまう
    # - logファイルが見つからない場合のException
    """
    
    filepath_ls = glob.glob(os.path.join(os.path.abspath(dirpath),"*"))
    filename_ls = [os.path.basename(p) for p in filepath_ls]
    
    change_ls = [] #(変更前, 変更後)のタプルのリスト
    for f in filename_ls:
        match = re.match(r'.*\.log.*', f)
        if match:
            tar = match.group()
            change_ls.append((tar, newlogfilename(tar, base)))
    
    tar_ls = []
    for change in change_ls:
        tar = os.path.join(os.path.abspath(dirpath), change[1])
        tar_ls.append(tar)
        os.rename(os.path.join(os.path.abspath(dirpath), change[0])
                  , tar)
        
    return tar_ls


class LogData():
    def __init__(self, logfilepath_ls):
        """
        Parameters
        ----------
        logfilepath_ls : list of path
            logファイルのパスのリスト
        """
        df_ls = []
        for path in logfilepath_ls:
            df_ls.append(pd.DataFrame(logfile_converter(path)))
        self._log_df = pd.concat(df_ls)
        
    @property
    def log_df(self):
        return copy.deepcopy(self._log_df)
        
    # [FutureWork]
    # def export_db(self):
    #     ...
    
    
if __name__ == "__main__":
    # print(pd.DataFrame(logfile_converter("loglog.log")))
    
    ld = LogData(["temp/templog.log"])
    pd = ld.log_df
    
    print(pd)