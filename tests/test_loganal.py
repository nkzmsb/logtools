import os

import pytest

from logtools.loganal import breakdown_values, expand_dict, keymake, log_to_dict, newlogfilename, renamefiles
from logtools.logging_tool import Logger

ATTRIBUTES = Logger().logsetting.attributes


@pytest.mark.parametrize("head, expect"
                         , [(None, "key"), ("h", "h-key")])
def test_keymake(head, expect):
    assert keymake("key", head) == expect


def test_expand_dict():
    dic = {"A" : 1, "Nest" : {"B" : "BBB", "C" : [3,4]}, "D" : (3,4,5)
           , "Nest2" : {"B2" : "QQQ", "C" : (3,4)}}
    
    expanded, remain = expand_dict(dic)
    
    assert expanded == {"A" : 1, "D" : (3,4,5)}
    assert remain == {"Nest" : {"B" : "BBB", "C" : [3,4]}
                      , "Nest2" : {"B2" : "QQQ", "C" : (3,4)}}
    
def test_expand_dict_withhead():
    dic = {"A" : 1, "Nest" : {"B" : "BBB", "C" : [3,4]}, "D" : (3,4,5)
           , "Nest2" : {"B2" : "QQQ", "C" : (3,4)}}
    
    expanded, remain = expand_dict(dic, "h-hh")
    
    assert expanded == {"h-hh-A" : 1, "h-hh-D" : (3,4,5)}
    assert remain == {"h-hh-Nest" : {"B" : "BBB", "C" : [3,4]}
                      , "h-hh-Nest2" : {"B2" : "QQQ", "C" : (3,4)}}

def test_breakdown_values():
    values = ("{'A': 'AAA', 'int': 3,"
              " 'nest': {'A': 'nestA', 'BB': {'bnest': [1, 2, 3], 'tag': True}}}")
    expect = {"A":"AAA"
              , "int" : 3
              , "nest-A" : "nestA"
              , "nest-BB-bnest" : [1, 2, 3]
              , "nest-BB-tag" : True}
    
    assert breakdown_values(values) == expect
    
def test_breakdown_values_none():    
    assert breakdown_values("None") == None

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
                   , "convert_exception" : "values warning"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("values is not valid but work")
    
    
def test_breakdown_values_warning_SE(recwarn):
    # [ToDo] np.arrayを含んでいても無理
    values = "{'int': 3, 'ndarray': array([[1, 2, 3],"
    
    ret = breakdown_values(values)
    
    assert len(recwarn) == 1
    assert ret == {"values" : values, "convert_exception" : "values error"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("values is not valid")


def test_log_to_dict(valid_typ_log):
    expect = {"asctime":"2021-05-09 16:30:12,093"
              , "levelname" : "INFO"
              , "name" : "DUMMYLOG"
              , "function" : "FUNC"
              , "action":"run"
              , "exception": "dummyError : [-1, -1, -1]"
              , "message" : "valid_typ_log"
              , "tag":None
              , "A":"AAA"
              , "int" : 3
              , "nest-A" : "nestA"
              , "nest-BB-bnest" : [1, 2, 3]
              , "nest-BB-tag" : True
              }
    
    assert log_to_dict(valid_typ_log) == expect
    
def test_log_to_dict_formaterror(recwarn, invalid_short_log):
    
    ret = log_to_dict(invalid_short_log)
    
    assert len(recwarn) == 1
    assert ret == {"values" : invalid_short_log, "convert_exception" : "strange format"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("strange format")

@pytest.mark.skip(reason="面倒なので未実装")
def test_logfile_converter():
    # データとexpectの準備が面倒くさい
    ...

def test_newlogfilename():
    assert newlogfilename("abc.log.4", "opq") == "opq_4.log"
    assert newlogfilename("abc.log", "opq") == "opq_0.log"
    assert newlogfilename("/bbb/abc.log.4", "opq") == "opq_4.log"
    assert newlogfilename("/bbb/abc.log", "opq") == "opq_0.log"
    

def test_renamefiles(tmpdir):
    # 一時フォルダにlogdata.log, logdata.log.1, logdata.log.2を準備する
    # 処理後に、after_0.log, after_1.log, after_2.logになっていることを確認する
    
    f1 = tmpdir.join("abc.log")
    f2 = tmpdir.join("abc.log.1")
    f3 = tmpdir.join("abc.log.2")
    f1.write("I am f1")
    f2.write("I am f2")
    f3.write("I am f3")
    
    ret = renamefiles(tmpdir, "after")
    
    res = set([os.path.abspath(p) for p in tmpdir.listdir()])
    expect = set([os.path.join(tmpdir, "after_0.log")
                  , os.path.join(tmpdir, "after_1.log")
                  , os.path.join(tmpdir, "after_2.log")])
    
    assert res == expect
    assert set(ret) == expect
    

@pytest.mark.skip(reason="面倒なので未実装")
class TestLogData():
    ...

# [ToDo]以下の項目でExceptionのテストが必要
# Warning
# - /そもそも入りが違う(@log_to_dict)
# - /項目の数が違う(@log_to_dict)
# - /ast.literal_evalのSyntaxError(@breakdown_values)
# Exception
# - [FW]ログファイルが見つからない(@renamefiles)



# ===参考
# def test_AAA(dummylog_unit):
#     avl_log = dummylog_unit["avl_log"]
#     assert avl_log.read() == 'DEBUG===run===None==={A:"A"}'