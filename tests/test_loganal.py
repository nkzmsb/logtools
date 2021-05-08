
import pytest

def test_dummylogs(valid_log):
    """fixtureのダミーログが正しく作れていることを確認する
    
    引数のfixtureはconftest.pyで定義されている
    （fixtureの使い方の練習も兼ねて）
    """
    
    assert valid_log == "2021-05-08 21:57:23,823___INFO___DUMMYLOG___FUNC___run___None___d_message___None___{'A': 'AAA', 'int': 3}"


# ===参考
# def test_AAA(dummylog_unit):
#     avl_log = dummylog_unit["avl_log"]
#     assert avl_log.read() == 'DEBUG___run___None___{A:"A"}'