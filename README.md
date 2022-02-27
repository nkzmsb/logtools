
# logtoolsとは
ログを規格化することで、統一的にログを扱う。

# Install
## pip
1. インストールしたい環境を立ち上げる
1. 下記requirementsに記載の一般ライブラリをインストール
1. logtoolsのアーカイブファイル(tar.gz)を配置したディレクトリ(ここではdistとした)の一つ上の階層に移動する。ls(windowsではdir)でdistが見えている状態
1. 以下のコマンドでインストールを行う
    ```
    $ pip install --no-index --find-links=dist logtools
    ```

**Notice**  
本パッケージはpipでインストールされることを想定しており、また、conda環境で使用されることも想定している。このインストーラにrequirements情報を含むと、自動的にインストールされたライブラリがconda環境と競合する恐れがある。したがって、本パッケージのインストーラにはrequirements情報は含んでいない。  
**ユーザーはインストールの際に、以下のrequirementの項を参考に手動で環境を構築する必要がある。**  

**issue**  
tar.gzファイルにはこのREADMEも含めて、データファイルが含まれているが、上記コマンドで実行しても、データファイルはsite-packages/logtoolsには展開されない。  
tar.gzはwindowsであってもpowershellを使えば以下コマンドでその場に解凍できる。（pathがターゲットのtar.gzに通っていることと、tar.gzの名前は適宜変更すること）  
```
$ tar -xzvf .\logtools-0.0.11.tar.gz
```


## requirements
以下の環境をインストール時に手動で構築する必要がある。
- python >= 3.7 : 辞書の並び情報とdataclassesを使用
- pandas : ログを行うだけの場合(loganalを利用しない場合)は不要


# logging_tool : ログを行う
## ロガーの設定(main)
本パッケージを使用するかどうかにかかわらず、ロギングを行う際には、メインモジュールでロガーの設定を行う必要がある。

### 簡易設定
jupyter等でファイル内で定義したロガーだけを使用すればよい場合には、以下のような簡易的な設定をする。
```python
import logging

import logtools # このパッケージ

# logtools.Logger.makeformat(attributes=..., splitter=...) # デフォルトのフォーマットを使う場合は不要
logger = logtools.getLogger(__name__)
logger.setLevel(logging.INFO) # ログレベルの設定
logger.add_StreamHandler() # デフォルトの画面出力ハンドラ設定
```


### 詳細設定
アプリケーションコード等のログ設定は、以下のようにdictConfigを使用して設定する。
dictConfigに渡す辞書は、yamlファイル等を読み込んだものを使用してもよい。
(https://docs.python.org/ja/3/library/logging.config.html)  

フォーマットを指定する際にはLoggerクラスのmakeformatクラスメソッドを使うことで、
Formatterに指定できるフォーマット形式を生成することができる。

```python
import logging, logging.config

import logtools # このパッケージ

logger = logtools.getLogger(__name__)

# フォーマットをデフォルト値と変更する場合には、
# makeformatの引数を設定する。
format = logtools.Logger.makeformat().format

conf_dic = {"version" : 1
            , "formatters" : {"default" : {"format" : format}}
            , "handlers" : {"console" : {"class" : "logging.StreamHandler"
                                         , "formatter" : "default"}
                            , "file" : {"class" : "logging.handlers.RotatingFileHandler"
                                        , "formatter" : "default"
                                        , "filename" : "logfolder/logfile.log"
                                        , "maxBytes" : 1000
                                        , "backupCount" : 3}}
            , "loggers" : {"__main__" : {"level" : "DEBUG"
                                    , "handlers" : ["console", "file"]}
                           }
            }

logging.config.dictConfig(conf_dic)
```

## ロギングを実施
### 基本的な利用方法
以下のように、モジュールへログコードを仕込む。
```python
import loglools

logger = loglools.getLogger(__name__)

logger.debug("aaa", action = "run", values = {"i" : 10})
logger.info("bbb", action = "finised", values = {"i" : 10})
logger.warning("ccc", values = {"val" : 5, "i" : 10})
logger.error("ddd", values = {"val" : 15, "i" : 10})
logger.critical("eee", values = {"val" : -5, "i" : 10})
```

### トレースデコレータ
関数やメソッドが呼ばれて、処理を終了したことを確認したい場合がある。
その際にはtrace_decoデコレータを使用することで、DEBUGレベルのトレースログを自動生成することができる。
```python
@logger.trace_deco
def demofunc():
    ...
    
class DemoClass():
    def __init__(self):
        ...
    
    @logger.trace_deco
    def demomethod(self):
        ...
```

### Logger.makeformat()クラスメソッド
フォーマットを確認したい場合と変更したい場合に利用する。
フォーマットを確認したい場合は、引数を与えずに実行し、返ってくる`LogSetting`インスタンスの、`format`属性や`attributes`・`splitter`属性で確認をする。  
フォーマットを変更したい場合は、[ロガーの設定(main)](#ロガーの設定main)の簡易設定・詳細設定で方法が異なるが該当サンプルコード内に記載の通り。

## ログ属性
ログのフォーマットには組み込み(logging)のログ属性と、logtoolsによって追加されたオリジナルのログ属性のうちから必要なものを選択して利用することができる。  
組み込みのログ属性は以下の通りで、詳細は[公式ドキュメント](https://docs.python.org/ja/3/library/logging.html#logrecord-attributes)を参考のこと。
```
"asctime", "created", "filename", "funcName"
"levelname", "levelno", "message", "module"
"msecs", "name", "pathname", "process"
"processName", "relativeCreated", "thread", "threadName"
```

オリジナルのログ属性は以下の通りで、詳細は[オリジナルのログ属性](#オリジナルのログ属性)を参考のこと。
```
"action", "exception", "function", "tag", "values"
```

## オリジナルのログ属性
ログレベルごとにログする属性が制限されている。すべてのログレベルには"messages"と"values"が設けられており、これを用いることによって、ログ形式の統一性を保ちつつ、ログ内容の自由度を担保する。
### debug
- action : 処理のどのタイミングのログか。任意の文字列を指定できるが、ログの統一性を保つために、以下の4つの文字列を使用することを推奨する。
    - "run" : 処理の開始時のログに使用する
    - "finished" : 処理の終了時のログに使用する
    - "check" : 処理の途中の確認用のログに使用する
    - "ready" : 処理が待機状態に入る際のログに使用する
- message : 任意の文字列。
- tag : ロギングのフィルタやloganal.pyで解析する際のフィルタリングに使用するためのタグ。デフォルトはNone（引数を渡さない）。任意の文字列を指定できるが、ログの統一性を保つために、debugレベルでは以下の文字列を使用することを推奨する。
    - "trace" : ログが呼ばれたことを追跡するためだけのログであることを示すタグ。
- values : ログが呼ばれた時点の値を辞書型で格納する。

### info
- action : debugレベル参照
- message : debugレベル参照
- tag : ロギングのフィルタやloganal.pyで解析する際のフィルタリングに使用するためのタグ。デフォルトはNone（引数を渡さない）。任意の文字列を指定できるが、ログの統一性を保つために、infoレベルでは以下の文字列を使用することを推奨する。
    - "use" : 積極的にvaluesの値を利用することを示すタグ。
- values : debugレベル参照

### warning
- exception : 例外クラス名。
- message : 例外メッセージ。
- values : debugレベル参照

### error
- exception : 例外クラス名。
- message : 例外メッセージ。
- values : debugレベル参照

### critical
- exception : 例外クラス名。
- message : 例外メッセージ。
- values : debugレベル参照


## 使用上の注意・制限事項
- logging.Loggerでログされているモジュールのロガーに対して、logtoolsのフォーマットを適用したロガーを渡す。この場合、LogRecordにフォーマットが要求する属性がないのでエラーになる。
## ログの属性の制限
loganal.pyでは、loggign_toolsを用いて生成したログレコードを、FileHandlerやhandlers.RotatingFileHandlerで出力したテキストファイルを使用する。  
loganal.pyを正しく動作させるための要請として、ログの属性は以下のような制限を満たさなければならない。  
基本的には、loganalは各行をast.literal_evalで評価することによる制限である。

- 組み込み型以外の型を入力しない。numpy.ndarrayやpandas.DataFrame、あるいは自作したクラスなどをvaluesに渡したいことが考えられる。自然なのは、それらを組み込み型に変換することである。別の方法としては、file出力やpickleを使って情報を手動で出力し、そのファイル名をログメッセージに入れるという方法も考えられる。
- 改行コードを含まないこと
- 分離要のキー（デフォルトは"==="）を含まないこと



## Tips
### ログのフォーマット情報をログ
ログ情報を解析する際、特にフォーマットをlogtoolsのデフォルトから変更している場合は、
ログのフォーマット情報があることが好ましい。  
そのための方法として、mainのモジュール等でフォーマットの属性情報をログしておくとよい。
```python
logger = logtools.getLogger(__name__)
logger.info(message = "log format information", tag="use",action="ready"
            , values = {"attribute" : logtools.Logger.makeformat().attributes})
```
### numpy.ndarrayのリスト化
nympy.ndarrayはtolistメソッドによってリスト化することができる。
```
some_ndarray=np.array([[1,2,3], [1,1,1]])
logger.debug("how to log ndarray", action = "info", values = {"example" : some_ndarray.tolist()})
```

### errorのログ
引数のexceptionにはエラーの種類が、meesageにはエラーメッセージが格納されることが望ましい。  
```
try:
    1/0
except ZeroDivisionError as zde:
    logger.error(exception = zde.__class__.__name__    # >>> "ZeroDivisionError"
                 , message = zde    # >>> "division by zero"
                 )
```

### warningのログ
引数のexceptionには警告の種類が、meesageには警告メッセージが格納されることが望ましい。  
```
import warning

with warnings.catch_warnings(record=True) as wa:
    # これだとログしないと警告が隠蔽されてしまうのが問題
    warnings.warn("This is a warning example", FutureWarning)

for w in wa:
    logging.warning(exception = w.message.__class__.__name__    # >>> "FutureWarning"
                    , message = w.message    # "This is a warning example"
                    )
```


# loganal:ログを解析する
## LogToDfクラス
上記logtools.Loggerで取得した複数のログファイルを、pandas.DataFrameの形に集約・変換する。  
インスタンス化の際に、ログのフォーマット情報として、属性情報(attributes)と区切り文字情報(spritter)を指定する。
これらの値を指定しない場合は、logtools.Logger.makeformat()で取得されるフォーマット情報が用いられる。  
実際の変換作業は、LogToDf.convert()クラスで実施される。引数には集約・変換したいログファイルのパスのリストを指定する。出力されるDataFrameはログの属性に含まれると仮定されている"asctime"で昇順ソートされる。

### 利用方法
```python

from logtools.loganal import LogToDf

# デフォルトのフォーマットを用いて作成したログファイルであれば、
# LogToDfの引数は不要
attrs = ("asctime", "levelname", "levelno", "message")
split_by = "---"
log_to_df = LogToDf(attributes = attrs, splitter = split_by)

logfile_ls = ["./log/foo.log", "./log/foo.log2"]

log_df = log_to_df.convert(logfile_ls)

log_df.to_csv("log.csv", index=False)
```

### 使用上の注意
- 出力されたDataFrameにconvert_exception列が付加され、そこに"values error"や"values warning"が
入っていた場合、そのログの"values"の値が、正しく処理できなかった可能性があるので確認が必要。
このようなログがされている場合には、logtools.Loggerの使い方を誤っている可能性が高い。
- LogToDfに指定する属性や区切り文字は、処理するログファイルのものを指定すること。
これと一致していないと、出力DataFrameも正しく作成されない。
