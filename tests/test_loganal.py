
import pytest

from logtools.loganal import breakdown_values, expand_dict, keymake, log_to_dict
from logtools.default import default

DEFAULT = default()
ATTRIBUTES = DEFAULT["attributes"]
# FORMATTER = DEFAULT["formatter"]
# SPLITTER = DEFAULT["splitter"]

def test_dummylogs(valid_typ_log):
    """fixtureのダミーログが正しく作れていることを確認する
    
    引数のfixtureはconftest.pyで定義されている
    （fixtureの使い方の練習も兼ねて）
    """
    print(valid_typ_log)
    
    assert valid_typ_log == ("2021-05-08 21:57:23,823___INFO___DUMMYLOG"
                             "___FUNC___run___dummyError : [-1, -1, -1]___d_message___None___"
                             "{'A': 'AAA', 'int': 3, "
                             "'nest': {'A': 'nestA', "
                             "'BB': {'bnest': [1, 2, 3], 'tag': True}}}")

@pytest.mark.parametrize("head, expect"
                         , [(None, "key"), ("h", "h-key")])
def test_keymake(head, expect):
    assert keymake("key", head) == expect


def test_expand_dict():
    dic = {"A" : 1, "Nest" : {"B" : "BBB", "C" : [3,4]}, "D" : (3,4,5)}
    
    res, exist = expand_dict(dic)
    
    assert res == {"A" : 1, "Nest-B" : "BBB", "Nest-C" : [3,4], "D" : (3,4,5)}
    assert exist == False

def test_breakdown_values():
    values = ("{'A': 'AAA', 'int': 3,"
              " 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    expect = {"A":"AAA"
              , "int" : 3
              , "nest-A" : "nestA"
              , "nest-BB-bnest" : [1, 2, 3]
              , "nest-BB-tag" : True}
    
    assert breakdown_values(values) == expect

@pytest.mark.parametrize("values"
                         , [5
                            , 3.14
                            , (1,2)
                            , [1,2]
                            , [[1,2], [3,4]]
                            , True])
def test_breakdown_values_notdict(values, recwarn):
    # Only dict is valid as type of values
    # but some type is work
    
    ret = breakdown_values(str(values))
    assert len(recwarn) == 1
    assert ret == {"values" : values
                   , "values_breakdown_error" : "Warning"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("values is not valid but work")
    
    
def test_breakdown_values_warning_SE(recwarn):
    values = "{'int': 3, 'ndarray': array([[1, 2, 3],"
    
    ret = breakdown_values(values)
    
    assert len(recwarn) == 1
    assert ret == {"values" : values, "values_breakdown_error" : "Error"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("values is not valid")


@pytest.mark.skip(reason="未実装")
def test_log_to_dict(valid_typ_log):
    expect = {"asctime":"2021-05-08 21:57:23,823"
              , "levelname" : "INFO"
              , "name" : "DUMMYLOG"
              , "func" : "FUNC"
              , "action":"run"
              , "exception":None
              , "message" : "d_message"
              , "tag":None
              , "A":"AAA"
              , "int" : 3
              , "nest-A" : "nestA"
              , "nest-BB-bnest" : [1, 2, 3]
              , "nest-BB-tag" : True
              }
    
    assert log_to_dict(valid_typ_log) == expect

@pytest.mark.skip(reason="未実装")
def test_logfile_converter():
    # データとexpectの準備が面倒くさい
    ...

@pytest.mark.skip(reason="未実装")
def test_rename():
    # 一時フォルダにlogdata.log, logdata.log2, logdata.log3, dummy.txtを準備する
    # 処理後に、logdata_1.log, logdata_2.log, logdata_3.log, dummy.txtになっていることを確認する
    ...
    
    

# [ToDo]以下の項目でExceptionのテストが必要
# Warning
# - そもそも入りが違う(@log_to_dict)
# - 項目の数が違う(@log_to_dict)
# - /ast.literal_evalのSyntaxError(@breakdown_values)
# Exception
# - ログファイルが見つからない(@renamefiles)



# ===参考
# def test_AAA(dummylog_unit):
#     avl_log = dummylog_unit["avl_log"]
#     assert avl_log.read() == 'DEBUG___run___None___{A:"A"}'