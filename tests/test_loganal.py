
import pytest

from logtools.loganal import unitlog_converter
from logtools.default import default

DEFAULT = default()
ATTRIBUTES = DEFAULT["attributes"]
# FORMATTER = DEFAULT["formatter"]
# SPLITTER = DEFAULT["splitter"]

def test_dummylogs(valid_log):
    """fixtureのダミーログが正しく作れていることを確認する
    
    引数のfixtureはconftest.pyで定義されている
    （fixtureの使い方の練習も兼ねて）
    """
    print(valid_log)
    
    assert valid_log == ("2021-05-08 21:57:23,823___INFO___DUMMYLOG"
                         "___FUNC___run___None___d_message___None___"
                         "{'A': 'AAA', 'int': 3, "
                         "'nest': {'A': 'nestA', "
                         "'BB': {'bnest': [1, 2, 3], 'tag': True}}}")

# def test_unitlog_converter(valid_log):
#     expect = {"asctime":"2021-05-08 21:57:23,823"
#               , "levelname" : "INFO"
#               , "name" : "DUMMYLOG"
#               , "func" : "FUNC"
#               , "action":"run"
#               , "exception":None
#               , "message" : "d_message"
#               , "tag":None
#               , "A":"AAA"
#               , "int" : 3
#               }
#     
#     assert unitlog_converter(valid_log) == expect


# ===参考
# def test_AAA(dummylog_unit):
#     avl_log = dummylog_unit["avl_log"]
#     assert avl_log.read() == 'DEBUG___run___None___{A:"A"}'