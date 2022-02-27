
import pandas as pd
import pytest

from logtools.loganal import LogToDf
from logtools.loganal import breakdown_values, expand_dict, keymake, log_to_dict, logfile_converter
from logtools.logging_tool import Logger

@pytest.fixture(scope="class")
def default_attributes():
    return Logger.makeformat().attributes

@pytest.fixture(scope="class")
def default_splitter():
    return Logger.makeformat().splitter

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


def test_log_to_dict(valid_typ_log, default_attributes, default_splitter):
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
    
    assert log_to_dict(valid_typ_log, default_attributes, default_splitter) == expect
    
def test_log_to_dict_formaterror(recwarn, invalid_short_log, default_attributes, default_splitter):
    
    ret = log_to_dict(invalid_short_log, default_attributes, default_splitter)
    
    assert len(recwarn) == 1
    assert ret == {"values" : invalid_short_log, "convert_exception" : "strange format"}
    
    w = recwarn.pop()
    assert w.category(UserWarning)
    assert str(w.message)==("strange format")

def test_logfile_converter(logfile_dir, default_attributes, default_splitter):
    log_ls = logfile_converter(logfile_dir.join('logfile1.log'), default_attributes, default_splitter)
    
    assert log_ls[0]["message"] == "log from logger1 No.1"

class TestLogToDf():
    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        self.target = LogToDf()

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        del self.target
        
    def test_convert(self, logfile_dir):
        fn1 = str(logfile_dir.join('logfile1.log'))
        fn2 = str(logfile_dir.join('logfile2.log'))
        log_df = self.target.convert([fn2, fn1])
        
        expect_message = ["log from logger1 No.1", "log from logger1 No.2"
                          , "log from logger2 No.1", "log from logger2 No.2"]
        
        for tar, expect in zip(log_df["message"], expect_message):
            assert tar == expect
            
    def test_sort_exception(self):
        dummy_df = pd.DataFrame({"col1":[4,2,5], "col2":[5,6,7]}) # df does not have "asctime"
        
        with pytest.warns(UserWarning) as record:
            self.target._sort_by_time(dummy_df)

        assert len(record) == 1
        assert record[0].message.args[0] == "log data is not sorted."
        

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