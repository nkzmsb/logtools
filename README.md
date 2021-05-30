# logtools

# 概要
ログを規格化することで、統一的にログを扱う。

# Install
## pip

```
$ pip install XXXXXX
```

**[Notice]**  
本パッケージはpipでインストールされることを想定しており、また、conda環境で使用されることも想定している。このインストーラにrequirements情報を含むと、自動的にインストールされたライブラリがconda環境と競合する恐れがある。したがって、本パッケージのインストーラにはrequirements情報は含んでいない。  
**ユーザーはインストールの際に、以下のrequirementの項を参考に手動で環境を構築する必要がある。**


## requiraments
以下の環境をインストール時に手動で構築する必要がある。
- python >= 3.7 : 辞書の並び情報とdataclassesを使用
- pandas



# How To Use
## logging設定
本パッケージを使用するかどうかにかかわらず、ロギングを行う際には、ロガーの設定を行う必要がある。

## Log属性について


## logging_toolsの利用
### 基本的な利用方法


### トレースデコレータ


### 制限事項
#### クラスをそのままぶち込まない
変なの入られるとloganalで困っちゃう。file出力やpickleを使って情報を一時保存し、ファイル名をログメッセージに入れるとか。


## loganalの利用
### rename


### 利用方法


---



=========仕様===========
# 概要
## 要求
- ファイル出力されたlogをデータベース化(まずは簡易的にpandas.DataFrame)して、自由に情報をフィルタリングできるようにしたい
- トレース用のログを容易に発生させられるようにしたい
- ログを発生させる箇所の関数やクラス名の情報をログに含めたい（funcNameでは不十分）
- ロガーはlogger=logging.getLogger(#)で定義されるloggerと互換性を持つこと（このパッケージに不具合があっても、軽微な修正でデフォルトの機能でロギングが可能になるように）
- filerotateで作成されたlogファイルは拡張子が変なことになる。解析時にはこれをrenameする。
- ロガー側の処理では例外が発生しないこと（遮蔽すること）

## 解決方法
- 対象となるログに形式上の制限をかける。ロギング用のクラス・関数を作る。
- 上記制限を満たしたlogをデータベース化するモジュールを作成する
- トレース用のログをデコレータで発生させる
- 組み込みのinspectモジュールを使って呼び出し元の情報を取得し、ログに追加する
- ロギング用のクラスを作成。メソッドにdebug, info, warning, error, criticalを準備する
- rename用の関数を作る
- ロガー側の処理で例外の発生がないように実装

## 機能
- 形式上の制限に対応したログを発生させられるメソッドを準備。制限された属性はextra引数でログする。
- ログをデータベース化する関数orクラス
- トレース用のデコレータ
- 呼び出し元の情報を取得する関数を作成（メソッドではない）
- debug, info, warning, error, criticalログを発生させる同名のメソッド
- rename関数
- pytest(https://dev.classmethod.jp/articles/python_logcapture/)

# 設計
## ログの制限
ログは以下のようなフォーマットでファイル出力するものとする  
'%(asctime)s___%(levelname)s___%(name)s___%(func)s___%(action)s___%(exception)s___%(message)s___%(tag)s___%(values)s'  
ただし、この形式は、logging_tool.pyのATTRIBUTE変数で変更可能。  
- 項目の区切りは"___(アンダースコア３つ)"とする。messageやvalueには任意の文字列を入れられるが、アンダースコアを3つ以上続けることは禁止する。
- extraには以下のAttlibuteが設定されている
-- action : "run", "finished", "ready", "check"。[debug, info]
-- exception : 例外情報。[warning, error, critical]
-- func : 関数名。メソッドの場合は"クラス名.関数名"。[all]
-- tag : タグ。"trace"[debug任意], "use"[info任意]。
-- values : 任意の辞書。[任意]
- messageには文字列のみ
- [ToDo]valuesに含めることができる型はTBD

## パッケージ構成
logtools  

|-- logtools  
|   |-- __init__.py  
|   |-- logging_tool.py # ログを作成するモジュール  
|   `-- loganal.py # ログを解析するモジュール  

|-- tests  
|   |-- __init__.py  
|   |-- test_logging_tool.py  
|   `-- test_loganal.py  

|-- setup.py  
`-- readme.txt  

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
foo.log -> foo_1.log  
foo.log2 -> foo_2.log  
foo.log# -> foo_#.log  
[Notice]この関数の実行は１回のみ。複数回実施すると変なファイル名になる。


# SampleCode
## logging_toolモジュール
```python
@logger.trace_deco
def demofunc():
    logger.debug("in demofunc", action = "run", values = {"i" : 6})
        
class DemoClass():
    def __init__(self):
        logger.info("@DemoClass init")
        
    @logger.trace_deco
    def demomethod(self):
        logger.warning("@DemoClass method")
    
dc = DemoClass()
demofunc()
for i in range(2):
    logger.debug("aaa", action = "run", values = {"i" : i})
    logger.info("bbb", action = "finised", values = {"i" : i})
    logger.warning("ccc", values = {"val" : 5, "i" : i})
    logger.error("ddd", values = {"val" : 15, "i" : i})
    logger.critical("eee", values = {"val" : -5, "i" : i})
    time.sleep(1)
        
dc.demomethod()
```

## loganalモジュール
```python
from logtools import LogData, renamefiles

renamefiles("temp", "templog")
logdata = LogData(["temp/templog_1.log", "temp/templog_2.log"])
log_df = logdata.log_df
```


# 懸念点
- ファイル出力されたログはテキストなので、情報がもとに戻るとは限らない。ログデータへの制限と、例外処理の検討が必要。