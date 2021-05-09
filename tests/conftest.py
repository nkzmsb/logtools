# テスト用のダミーログファイル生成

import logging

import pytest

from logtools.default import default

FORMATTER = default()["formatter"]

@pytest.fixture(scope="module")
def valid_typ_log():
    """loganal.pyで取り扱えるタイプのログ（１つ）を作成する
    """
    ret = ("2021-05-09 16:30:12,093___INFO___DUMMYLOG___FUNC___"
           "run___dummyError : [-1, -1, -1]___valid_typ_log___None___"
           "{'A': 'AAA', 'int': 3, 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    
    return ret

def invalid_short_log():
    """フォーマットが異なり、loganal.pyで取り扱えないログ（１つ）を作成する
    """
    ret = ("INFO___invalid_short_log___"
           "{'A': 'AAA', 'int': 3, 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    
    return ret

# [ToDo] numpy件はtest_breakdown_values_warning_SEに追加する
# def invalid_np_log():
#     """valueが解析できずに、loganal.pyで取り扱えないログ（１つ）を作成する
#     """
#     
#     ret = ("2021-05-09 16:46:55,637___INFO___DUMMYLOG___FUNC___"
#            "run___dummyError : [-1, -1, -1]___invalid_np_log___None___"
#            "{'A': array([1, 2, 3])}")
#     
#     return ret
    

# ===参考===
# @pytest.fixture(scope="module")
# def dummylog_unit(tmpdir_factory):
#     unitlogs_dir = tmpdir_factory.mktemp("unitlogs")
#     
#     
#     avl_log = 'DEBUG___run___None___{A:"A"}'
#     avl_log_file = unitlogs_dir.join("avl_log.txt")
#     avl_log_file.write(avl_log)
#     
#     return {"avl_log":avl_log_file}
    

if __name__ == "__main__":
    print("hello")