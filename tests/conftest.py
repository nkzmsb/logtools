# テスト用のダミーログファイル生成

import logging

import pytest

from logtools.default import default

FORMATTER = default()["formatter"]

@pytest.fixture(scope="module")
def valid_typ_log(tmpdir_factory):
    """loganal.pyで取り扱えるタイプのログ（１つ）を作成する
    """
    temp_dir = tmpdir_factory.mktemp("temp_dir")
    temp_file = temp_dir.join("temp_file.log")
    
    logger = logging.getLogger("DUMMYLOG")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMATTER[14:]) # asctimeは固定値を付加するため削除
    handler = logging.FileHandler(temp_file)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    try:
        raise ValueError("dummyError : {}".format([-1,-1,-1]))
    except ValueError as ve:
        exc = ve
        
    
    dummy_extra = {"func":"FUNC", "action":"run", "exception":exc, "tag":None
                   , "values":{"A":"AAA"
                               , "int" : 3
                               , "nest" : {"A" : "nestA"
                                           , "BB" : {"bnest" : [1,2,3]
                                                     , "tag" : True}
                                           }
                               }
                   }
    logger.info("d_message", extra = dummy_extra)
    
    unitlog = temp_file.read()
    unitlog = "2021-05-08 21:57:23,823___" + unitlog # acstimeは固定値を付加
    
    return unitlog.replace( '\n' , '' )
    

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