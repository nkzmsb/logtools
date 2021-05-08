# logtools








=========仕様===========
# 概要
## 要求
- /ファイル出力されたlogをデータベース化(まずは簡易的にpandas.DataFrame)して、自由に情報をフィルタリングできるようにしたい
- /トレース用のログを容易に発生させられるようにしたい
- /ログを発生させる箇所の関数やクラス名の情報をログに含めたい（funcNameでは不十分）
- /ロガーはlogger=logging.getLogger(#)で定義されるloggerと互換性を持つこと（このパッケージに不具合があっても、軽微な修正でデフォルトの機能でロギングが可能になるように）
- /filerotateで作成されたlogファイルは拡張子が変なことになる。解析時にはこれをrenameする。
- /ロガー側の処理では例外が発生しないこと（遮蔽すること）

## 解決方法
- /対象となるログに形式上の制限をかける。必要に応じてロギング用のクラス・関数を作る。
- /上記制限を満たしたlogをデータベース化するモジュールを作成する
- /トレース用のログをデコレータで発生させる
- /組み込みのinspectモジュールを使って呼び出し元の情報を取得し、ログに追加する
- /ロギング用のクラスを作成。メソッドにdebug, info, warning, error, criticalを準備する
- /rename用の関数を作る
- /ロガー側の処理で例外の発生がありえるところはテスト。テストが難しいところはtry文でwarning発生

## 機能
- 制限に対応したログを発生させられるメソッド.制限はextra引数で
- ログをデータベース化する関数orクラス
- トレース用のデコレータ
- 呼び出し元の情報を取得する関数を作成（メソッドではない）
- debug, info, warning, error, criticalログを発生させる同名のメソッド
- 呼び出し元の情報を取得する関数
- rename関数
- pytest(https://dev.classmethod.jp/articles/python_logcapture/)

# 設計
## ログの制限
ログは以下のようなフォーマットでファイル出力するものとする  
'%(asctime)s___%(levelname)s___%(name)s___%(func)s___%(action)s___%(expection)s___%(message)s___%(tag)s___%(values)s'  
- 項目の区切りは"___(アンダースコア３つ)"とする。messageやvalueには任意の文字列を入れられるが、アンダースコアを3つ以上続けることは禁止する。
- extraには以下のAttlibuteが設定されている
-- action : "run", "finished", "ready", "check"。[debug, info]
-- expection : 例外情報。[warning, error, critical]
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
ログを生成するモジュール。例外発生で止まらないようにする必要がある。
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
Filerotateで変な名前になっているファイルをリネームする


# 懸念点
- ファイル出力されたログはテキストなので、情報がもとに戻るとは限らない。ログデータへの制限と、例外処理の検討が必要。