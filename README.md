# logtools

# 概要
ログを規格化することで、統一的にログを扱う。

# Install
## pip
インストールしたい環境を立ち上げた状態で、distファイルを置いたディレクトリに移動したのち、以下コマンドを実行。
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


## requiraments
以下の環境をインストール時に手動で構築する必要がある。
- python >= 3.7 : 辞書の並び情報とdataclassesを使用
- pandas


# How To Use
## logging設定(main)
本パッケージを使用するかどうかにかかわらず、ロギングを行う際には、メインモジュールでロガーの設定を行う必要がある。

### 簡易設定
jupyter等でファイル内で定義したロガーだけを使用すればよい場合には、以下のような簡易的な設定をする。
```python
import logging

import logtools # このパッケージ

logger = logtools.Logger(__name__)
logger.logger.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(logger.logsetting.format)
# create console handler
handler = logging.StreamHandler()
# add formatter to handler
handler.setFormatter(formatter)

# add handler to logger
logger.logger.addHandler(handler)
```


### 詳細設定
アプリケーションコード等のログ設定は、以下のようにdictConfigを使用して設定する。
dictConfigに渡す辞書は、yamlファイル等を読み込んだものを使用してもよい。
(https://docs.python.org/ja/3/library/logging.config.html)

```python
import logging, logging.config

import logtools # このパッケージ

logger = logtools.Logger(__name__)

conf_dic = {"version" : 1
            , "formatters" : {"default" : {"format" : logger.logsetting.format}}
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

## ログ属性
ログレベルごとにログする属性が制限されている。すべてのログレベルには"messages"と"values"が設けられており、これを用いることによって、ログ形式の統一性を保ちつつ、ログ内容の自由度を担保する。
### debug
- action : 処理のどのタイミングのログか。任意の文字列を指定できるが、ログの統一性を保つために、以下の4つの文字列を使用することを推奨する。
    - "run" : 処理の開始時のログに使用する
    - "finished" : 処理の終了時のログに使用する
    - "check" : 処理の途中の確認用のログに使用する
    - "ready" : 処理が待機状態に入る際のログに使用する
- function : ログが発生した関数の名前。指定しなければ自動的に追加されるため、普通はユーザーが指定する必要はない。
- message : 任意の文字列。
- tag : ロギングのフィルタやloganal.pyで解析する際のフィルタリングに使用するためのタグ。デフォルトはNone（引数を渡さない）。任意の文字列を指定できるが、ログの統一性を保つために、debugレベルでは以下の文字列を使用することを推奨する。
    - "trace" : ログが呼ばれたことを追跡するためだけのログであることを示すタグ。
- values : ログが呼ばれた時点の値を辞書型で格納する。

### info
- action : debugレベル参照
- function : debugレベル参照
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



## logging_toolsの利用
### 基本的な利用方法
以下のように、モジュールへログコードを仕込む。
```python
import loglools

logger = loglools.Logger(__name__)

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


### 制限事項
#### ログの属性の制限
loganal.pyでは、loggign_toolsを用いて生成したログレコードを、FileHandlerやhandlers.RotatingFileHandlerで出力したテキストファイルを使用する。  
loganal.pyを正しく動作させるための要請として、ログの属性は以下のような制限を満たさなければならない。  
基本的には、loganalは各行をast.literal_evalで評価することによる制限である。

- 組み込み型以外の型を入力しない。numpy.ndarrayやpandas.DataFrame、あるいは自作したクラスなどをvaluesに渡したいことが考えられる。自然なのは、それらを組み込み型に変換することである。別の方法としては、file出力やpickleを使って情報を手動で出力し、そのファイル名をログメッセージに入れるという方法も考えられる。
- 改行コードを含まないこと
- 分離要のキー（デフォルトは"==="）を含まないこと


### Tips
#### numpy.ndarrayのリスト化
nympy.ndarrayはtolistメソッドによってリスト化することができる。
```
some_ndarray=np.array([[1,2,3], [1,1,1]])
logger.debug("how to log ndarray", action = "info", values = {"example" : some_ndarray.tolist()})
```

#### errorのログ
引数のexceptionにはエラーの種類が、meesageにはエラーメッセージが格納されることが望ましい。  
```
try:
    1/0
except ZeroDivisionError as zde:
    logger.error(exception = zde.__class__.__name__    # >>> "ZeroDivisionError"
                 , message = zde    # >>> "division by zero"
                 )
```

#### warningのログ
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


## loganalの利用
### renamefiles
logging.handlers.RotatingFileHandlerのbackupCount引数を指定して、ログファイルを生成した場合、複数のファイルが生成されるが、ファイル名の最後に".#"というファイル番号を示す文字列が付加されてしまう。
これを"*_#.log"というファイル名に変更する。  
【Note】RotatingFileHandlerのfilename引数には、"*.log"というファイル名を指定すること。（内部で".log"という文字列をキーにして解析するため）

### 利用方法
loganalの中で使用するのはrenamefiles関数と、LogDataクラスである。
```python
import glob
import os

import pandas as pd

import logtools

# ここではサンプルコードのためrenamefilesを解析用のプログラムに組み込んでいるが、
# renamefilesは1度実行すれば十分なので、独立の処理とすべき
logtools.renamefiles("./logfolder", "renamelog")

logfile_ls = [os.path.abspath(path) for path in glob.glob("./logfolder/*.log")]

data = logtools.LogData(logfile_ls)

df = data.log_df
```

# Advanced info
- logging_tool内のグローバル変数やコードを変更することで、ログの形式を変更することは可能。ただし、本パッケージの目的は、ログを規格化することなので、ユーザーが個々でこれらを編集することは非推奨。

# ToDo/Issue
- ロギングの属性はある程度変更できるようにしておいたほうが良い(組み込み属性の追加・削除)。例えば"threadName"はマルチスレッドのアプリだとが欲しいが、それ以外だと不要。この辺りまでは柔軟に対応できるようにしたい。
- ファイル出力されたログはテキストなので、情報がもとに戻るとは限らない。ログデータへの制限と、例外処理の検討が必要。
- 元のloggerと似た感じにはなっているが、元のloggerの引数にtagなどの新しく付け加えたものはないのでエラーが出る。こういうものとしてあきらめるか、対策を考えてアップデートするか。
- loganal.renamefilesにファイル名のチェック機能を入れたほうが良い。
- パッケージングのベストプラクティスを確認
- logがハンドリングされる順番がlogイベントが発生した順番とは限らない。loganal.LogDataでは時間順にDataFrameをソートしてあげるほうが親切かも。
- jupyter等で使う際の設定部分のボイラーコード、どうにかならないか要検討。


---
# 設計
以下は設計情報
## 要求
### 対応済
- ファイル出力されたlogをデータベース化(まずは簡易的にpandas.DataFrame)して、自由に情報をフィルタリングできるようにしたい
- トレース用のログを容易に発生させられるようにしたい
- ログを発生させる箇所の関数やクラス名の情報をログに含めたい（funcNameでは不十分）
- filerotateで作成されたlogファイルは拡張子が変なことになる。解析時にはこれをrenameする。

### 未対応
- ロガーはlogger=logging.getLogger(#)で定義されるloggerと互換性を持つこと（このパッケージに不具合があっても、軽微な修正でデフォルトの機能でロギングが可能になるように）
- 【動作未確認】ロガー側の処理では例外が発生しないこと（遮蔽すること）
- 【動作未確認】スレッドセーフであること

## 方針
- 対象となるログに形式上の制限をかける。ロギング用のクラス・関数を作る。
- 上記制限を満たしたlogをデータベース化するモジュールを作成する
- トレース用のログをデコレータで発生させる
- 組み込みのinspectモジュールを使って呼び出し元の情報を取得し、ログに追加する
- ロギング用のクラスを作成。メソッドにdebug, info, warning, error, criticalを準備する
- rename用の関数を作る
- ロガー側の処理で例外の発生がないように実装

## ログの制限
ログは以下のようなフォーマットでファイル出力するものとする  
'%(asctime)s===%(levelname)s===%(name)s===%(func)s===%(action)s===%(exception)s===%(message)s===%(tag)s===%(values)s'  
ただし、この形式は、logging_tool.pyのATTRIBUTE変数で変更可能。  
- 項目の区切りは"===(イコール記号３つ)"とする。messageやvalueには任意の文字列を入れられるが、イコール記号を3つ以上続けること、末尾にイコール記号を使用することは禁止する。
- extraには以下のAttlibuteが設定されている
-- action : "run", "finished", "ready", "check"。[debug, info]
-- exception : 例外情報。[warning, error, critical]
-- func : 関数名。メソッドの場合は"クラス名.関数名"。[all]
-- tag : タグ。"trace"[debug任意], "use"[info任意]。
-- values : 任意の辞書。[任意]
- messageには文字列のみ
- valuesには辞書型

## パッケージ構成
logtools  

|-- logtools  
|   |-- \_\_init__.py  
|   |-- logging_tool.py # ログを作成するモジュール  
|   `-- loganal.py # ログを解析するモジュール  

|-- tests  
|   |-- \_\_init__.py  
|   |-- conftest.py  
|   |-- test_logging_tool.py  
|   `-- test_loganal.py  

|-- setup.py  
`-- README.md  

## logging_toolモジュール
ログを生成するモジュール。生成するログの形式はATTRIBUTESとSPLITTERで定義する。

### Loggerクラス
インスタンス時にlogging.Loggerを作成し、そのLoggerを使って形式に合致したログを発生させる。
- logger（プロパティ）:logging.Loggerのインスタンスを返す。形式を無視したログを発生させたい場合に使用。
- log_deco（デコレータ）:トレース用のデコレータ
- debug : デバッグログを作成
- info : インフォログを作成
- warning : warningログを生成
- error : errorログを生成
- critical : criticalログを生成
### get_funcname関数
inspectモジュールを使って、呼び出し元の関数名（メソッド名）を取得する。
Loggerクラス内での使用と、この関数単独での使用を想定する。

## loganalモジュール
logging_tool.Loggerでファイル出力されたログを分析するためのユーティリティ。
### LogDataクラス
ログファイルを読み込んでpandas.DataFrame化する。必要に応じて、データフレームの作成も検討する。
- log_df（プロパティ）:読み込んだログデータのデータフレーム（コピー）
- export_db : [TBD] データベースへの出力

### rename関数
Filerotateで変な名前になっているファイルをリネームする。
foo.log -> foo_0.log  
foo.log.1 -> foo_1.log  
foo.log.2 -> foo_#.log  
[Notice]この関数の実行は１回のみ。複数回実施すると変なファイル名になる。

