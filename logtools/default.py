# 対象とするフォーマットのデフォルトを設定する
# コードの冗長性をなくす目的のモジュール。積極的な変更は想定しない。
# 基本的にはこのフォーマットを使うため、テストはこのデフォルトフォーマットに対してのみ行う

# ログに含める属性
# この順番通りにログが作成される
ATTRIBUTES = tuple(["asctime", "levelname", "name", "func"
                    , "action", "exception", "message", "tag", "values"
                    ])

# 各属性のスプリッター
SPLITTER = "___"

FORMATTER = ""

#####################################################
# ここまでが設定
# ここから下はルーチン処理
#####################################################

# 用意されている属性
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
ATTRIBUTE_BUILT_IN_ALL = ["asctime", "created", "filename", "funcName"
                          , "levelname", "levelno", "message", "module"
                          , "msecs", "name", "pathname", "process", "processName"
                          , "relativeCreated", "thread", "threadName"]


def classified_attr():
    """ATTRIBUTESをATTRIBUTE_BUILT_IN_ALLに含まれるものとそうでないものに分類する

    Returns
    -------
    attribute_buildin： tuple
        ATTRIBUTE_BUILT_IN_ALLに含まれる属性
    attribute_extra: tuple
        ATTRIBUTE_BUILT_IN_ALLに含まれない属性
    """
    all_use_set = set(ATTRIBUTES)
    all_builtin_set = set(ATTRIBUTE_BUILT_IN_ALL)
    
    attribute_buildin = tuple(sorted(all_use_set&all_builtin_set
                                     , key = ATTRIBUTES.index))
    attribute_extra = tuple(sorted(all_use_set-all_builtin_set
                                   , key = ATTRIBUTES.index))
    
    return attribute_buildin, attribute_extra


attribute_buildin, attribute_extra = classified_attr()

for i, attrib in enumerate(ATTRIBUTES):
    FORMATTER += "%({})s".format(attrib)
    if i < len(ATTRIBUTES) - 1:
        FORMATTER += SPLITTER

def default():
    """デフォルト値を返す

    attribute : ロギングする属性（項目）
    formatter : ロギングのフォーマット。ハンドラにsetされることを想定している。
    splitter : ロギング属性を分けるスプリッター
    """
    dic = {"attributes" : ATTRIBUTES
           , "attribute_buildin" : attribute_buildin
           , "attribute_extra" : attribute_extra
           , "formatter" : FORMATTER
           , "splitter" : SPLITTER}
    return dic


if __name__ == "__main__":
    l1 = (5,-4,1,2,-2,3,10)
    s1 = set(l1)
    
    l2 = [6,5,7,4,8,3,9,2,1]
    s2 = set(l2)
    
    print(sorted(s1&s2, key = l1.index))
    print(sorted(s1-s2, key = l1.index))
    
    print(default())