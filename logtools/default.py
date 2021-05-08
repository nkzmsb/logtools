# 対象とするフォーマットのデフォルトを設定する
# コードの冗長性をなくす目的のモジュール。積極的な変更は想定しない。
# 基本的にはこのフォーマットを使うため、テストはこのデフォルトフォーマットに対してのみ行う

# "asctime", "levelname", "name", "message"は組み込み
# それ以外はextra引数で指定
attributes = tuple(["asctime", "levelname", "name", "func"
                    , "action", "exception", "message", "tag", "values"
                    ])

# 各属性のスプリッター
splitter = "___"

formatter = ""
for i, attrib in enumerate(attributes):
    formatter += "%({})s".format(attrib)
    if i < len(attributes) - 1:
        formatter += splitter

def default():
    """デフォルト値を返す

    attribute : ロギングする属性（項目）
    formatter : ロギングのフォーマット。ハンドラにsetされることを想定している。
    splitter : ロギング属性を分けるスプリッター
    """
    dic = {"attributes" : attributes
           , "formatter" : formatter
           , "splitter" : splitter}
    return dic

if __name__ == "__main__":
    de = default()
    print("attributes : ", de["attributes"])
    print("formatter : ", de["formatter"])