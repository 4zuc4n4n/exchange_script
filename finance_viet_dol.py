#■作業流れ
#GCPプロジェクト立ち上げ
#Google Sheets APIの有効化、秘密鍵作成
#Googleスプレッドシートで為替情報を入力、レートを出力しておく
#使用するサーバーにpythonやスプレッドシートのライブラリをインストール
#作った秘密鍵を任意の場所に保存
#コード作成　API接続コードとスプレッドシートにある任意のセルの内容が出力できるコードを書く(このファイル)
#APIとサーバーの疎通確認


# coding: UTF-8
import os
#Pythonのコード上でOSに関する操作を実現するためのモジュール 使用しない
import json
#json操作用のライブラリ　使用しない
#GoogleスプレッドシートをPythonで操作することが可能になるライブラリ
import gspread
#googleのoauth2clientというライブラリ内のServiceAccountCredentialsという関数だけをインポート
from oauth2client.service_account import ServiceAccountCredentials
#日付取得用モジュール
import datetime
#pythonでMySQLを使用するためのライブラリ
import MySQLdb

#データベース接続
connection = MySQLdb.connect(
host='サーバーホスト名',
user='MySQLユーザー名',
passwd='上記ユーザーのパスワード',
db='登録先データベース名')
cursor = connection.cursor()

#googlespreadsheetのAPIへアクセスするためのキー ※為替の取得関連はSpreadsheet内で行っている
ACCESS_KEY_JSON = '/var/www/html/key/finance_viet_dol/ocrtest-336408-fc27fc519a23.json'
SPREAD_SHEET_KEY = "1U1AcY-1BA_vFenp0sb7cLMFMH4bHMSjsWl4PSbqbx9g"

#pairカラムに入れる値
pair = str('USDVND')

#rateカラムに入れる値
#キーを使い認証設定取得
credentials = ServiceAccountCredentials.from_json_keyfile_name(ACCESS_KEY_JSON, ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'])
#取得した認証設定でSpreadsheetの実ファイルに接続
worksheet = gspread.authorize(credentials).open_by_key(SPREAD_SHEET_KEY).sheet1
#実ファイル内のセル"C2"の値を取得
rate = worksheet.acell('C2').value

#ratedateに入れる値
ratedate = str(datetime.date.today())

#DBに登録されている最新のレート日時を取得
sql00 = 'SELECT 登録先テーブル.登録済みデータが記録されるカラム名 FROM 録先テーブル ORDER BY 登録済みデータが記録されるカラム名 DESC LIMIT 1'
cursor.execute(sql00)
# fetchone()で1件ずつ取り出し
rows = cursor.fetchone()[0]
#SQL実行
connection.commit()
#取得した最新のインサート日時を変数に記録
check_date = rows.strftime('%Y-%m-%d')

#既にデータベースに当日のレートがインサートされていないか確認を行う
if check_date != ratedate:
    #データ未インサートなので、データベースへインサートを行う
    #取得した値を登録先テーブルにインサート
    es = "'"
    sql01 = 'INSERT into 登録先テーブル(pair,rate,ratedate) VALUES (' + es + pair + es + ','+ es + rate + es + ',' + es + ratedate+ es + ')'
    #print(sql01)
    cursor.execute(sql01)
    
    #SQL実行
    connection.commit()
    #SQL切断
    connection.close()
else:
    #既にデータがあるので、現在のレートをphpへ渡す
    #SQL切断
    connection.close()
    #テスト用、テキストファイルで出力
    print(rate)