## 学習メモ
PythonServer

参考

https://pymori.xyz/2izb2dwpum/#toc18

手順

１．必要なライブラリのインポート

ソケットを実装するためにsocketライブラリをインポートする

２．ソケットの作成とホスト名の取得

socket()関数はソケット生成のためのソケットライブラリのコンストラクタ

ソケット生成時にホスト名/デバイス名をgethostname()で取得する

ポートは任意のポートを指定できる

３．ホストとポートのバインド

new socketに対して呼び出されるbind関数を用いて、ホストとポートをバインドする。

４．コネクションを聴く

listen()関数を使用する

この関数はnumber of connections という1つの引数を受け取る

５．着信接続を受け入れる

connがソケットに接続され、変数’add’がクライアントのIPアドレスに割り当てられる

６，着信接続データの保存

受信した接続の詳細はclient_name変数に格納される

サーバでデコードされ、接続された旨のメッセージが表示される。

サーバはホスト名を送信する

７．パケット/メッセージの配送

ユーザはメッセージを入力する

メッセージはencode()によってエンコードされ、ソケットを介して送信される

メッセージの送受信は、accept()関数の呼び出しで生成されたコネクションオブジェクト上でsend()関数を用いて行われる

受信したメッセージはconnオブジェクトのrecv()を使って受信する

メッセージはサーバ側でdecode()を用いて復号される


Vue.js

参考

https://qiita.com/tky_st/items/03faba81129e4877c3ea

https://qiita.com/tykt/items/5fa6140553e64dab88be

Vue.jeの初期設定

公式サイトに従ってインストールする

$npm install -g @vue/cli

プロジェクトを作成する

$vue create frontend

コンソールに選択肢が出てくるため、Manually select featuresを選択し、Vuexを追加で選択

Vue.jsのバージョンを選択する。

ESlintの設定を選択する。

Lintをかけるタイミングを選択する。

各種設定をどこに置くか選択する。

設定をプリセットとして保存するか選択する。

プロジェクトを作成出来たらコマンドを入力しhttp://localhost:8080　にアクセスする。

$ cd frontend/

$ npm run serve

Vuetifyを利用するためにインストールする。

$ vue add vuetify

