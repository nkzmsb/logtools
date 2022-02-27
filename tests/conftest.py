# テスト用のダミーログファイル生成
import logging.config
import time

import pytest

import logtools

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

@pytest.fixture(scope='session')
def logfile_dir(tmpdir_factory):
    """一時ディレクトリに、2種類のログファイルを生成する

    Returns
    -------
    Path
        logfile1.logとlogfile2.logが格納された
        一時ディレクトリのパス
    """
    dir_path = tmpdir_factory.mktemp('log')
    fn1 = str(dir_path.join('logfile1.log'))
    fn2 = str(dir_path.join('logfile2.log'))
    
    logger1 = logtools.getLogger("log1_logger")
    logger2 = logtools.getLogger("log2_logger")
    
    format = logtools.Logger.makeformat().format
    conf_dic = {"version" : 1
                , "formatters" : {"default" : {"format" : format}}
                , "handlers" : {"file1" : {"class" : "logging.handlers.RotatingFileHandler"
                                           , "formatter" : "default"
                                           , "filename" : fn1
                                           , "maxBytes" : 1000
                                           , "backupCount" : 1}
                                , "file2" : {"class" : "logging.handlers.RotatingFileHandler"
                                             , "formatter" : "default"
                                             , "filename" : fn2
                                             , "maxBytes" : 1000
                                             , "backupCount" : 1}}
                , "loggers" : {"log1_logger" : {"level" : "DEBUG", "handlers" : ["file1"]}
                               , "log2_logger" : {"level" : "DEBUG", "handlers" : ["file2"]}
                               }
                }
    logging.config.dictConfig(conf_dic)
    
    logger1.info("log from logger1 No.1")
    time.sleep(0.2) # logの時間や順序付けが明確になるように（おまじない）
    logger1.info("log from logger1 No.2")
    time.sleep(0.2)
    logger2.info("log from logger2 No.1")
    time.sleep(0.2)
    logger2.info("log from logger2 No.2")
    
    return dir_path

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