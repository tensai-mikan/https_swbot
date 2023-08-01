# https通信からswitchbotを動かす
こんにちは。今回は、前に書いたnote[100均のリモコンからIoT始めた](https://note.com/temiteria/n/n689d759b3757)の部分の一部をまとめようと思いまして。書いてから1か月以上もたってしまいましたが、残しておいた方が良いかなぁって。  
何かの参考になればうれしいです。

## 使用した言語
node.jsとpythonの２つ。node.jsのバージョンはv18.16.1で、pythonは3.11.4です。
バージョン依存のコードはそんなにないと思いますので、わざわざnodenvとかanacondaとかでバージョンをそろえたりしなくても動くかとは思いますが一応書いておきます。

## 大雑把な仕組み
まず、node.jsを使ってhttps通信で必要なパラメーターをサーバーに渡します。そのあと、pythonに引き渡してswitchbotを動かします。

## https通信でサーバーにリクエスト
getを使って、keyにパスワード、qに実行させたい命令を入れます。qに入れる命令というのは、device.jsonにあります。plug1-toggleとかです。

## switchbotとの通信
サーバーとswitchbot間には、bluetoothを使用します。[公式のAPI](https://github.com/OpenWonderLabs/python-host)のswitchbot_py3.pyを覗いてみると、switchbotに送れる通信は全部で6種類、press, on, off, open, close, pauseだそうです。  
pythonでの実装については、qittaの[SwitchBotをWindows 10 から制御する](https://qiita.com/hiratarich/items/00be23735ac6001ff74b)が参考になりました。

## device.jsonについて
これは、先ほど述べたswitchbotとの6種の通信の名前と、動かしたいswitchbotのMACアドレスを２つセットにしておくためのものです。
これで、https通信の時、「動かしたい機器」と「送る内容」の２つを送るのではなく、「実行させたい命令」の１つのパラメーターで済むようになります。まあ、もうすこしいい実装があったかもしれませんが。

## パスワードについて
インターネット経由でswitchbotを動かすことになりますので、自分のIPなどが分かってしまえば、第三者からの操作ができるようになってしまいます。それでいいならいいですが、当然嫌です。そのため、httpsするとき、keyのパラメーターに自分しかわからないパスワードを送って認証を行います。パスワードを保存する時は、server.jsに直でパスワードを置いておくのもありですし、pw.txtに保存しておくのもあり。ただし、ハッシュ化して置いておくべきですね。(私はやってませんが)
