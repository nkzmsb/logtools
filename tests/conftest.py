# テスト用のダミーログファイル生成

import logging

import pytest
from testfixtures import LogCapture

from logtools.logging_tool import Logger

FORMATTER = Logger().logsetting.format

@pytest.fixture(scope="module")
def valid_typ_log():
    """loganal.pyで取り扱えるタイプのログ（１つ）を作成する
    """
    ret = ("2021-05-09 16:30:12,093===INFO===DUMMYLOG===FUNC==="
           "run===dummyError : [-1, -1, -1]===valid_typ_log===None==="
           "{'A': 'AAA', 'int': 3, 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    
    return ret

@pytest.fixture(scope="module")
def invalid_short_log():
    """フォーマットが異なり、loganal.pyで取り扱えないログ（１つ）を作成する
    """
    ret = ("INFO===invalid_short_log==="
           "{'A': 'AAA', 'int': 3, 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    
    return ret

# [FutureWork] numpy件はtest_breakdown_values_warning_SEに追加する
# def invalid_np_log():
#     """valueが解析できずに、loganal.pyで取り扱えないログ（１つ）を作成する
#     """
#     
#     ret = ("2021-05-09 16:46:55,637===INFO===DUMMYLOG===FUNC==="
#            "run===dummyError : [-1, -1, -1]===invalid_np_log===None==="
#            "{'A': array([1, 2, 3])}")
#     
#     return ret
    

# ===参考===
# @pytest.fixture(scope="module")
# def dummylog_unit(tmpdir_factory):
#     unitlogs_dir = tmpdir_factory.mktemp("unitlogs")
#     
#     
#     avl_log = 'DEBUG===run===None==={A:"A"}'
#     avl_log_file = unitlogs_dir.join("avl_log.txt")
#     avl_log_file.write(avl_log)
#     
#     return {"avl_log":avl_log_file}
    

        
if __name__ == "__main__":
    print("hello")