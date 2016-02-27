Entrance Monitor
======================
玄関(覗き穴)から取得した映像(Raspberry Pi + [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer) を想定)について，動体検知された時に画像を保存します．

動作環境
------
* python 2.7.6
* python-opencv 2.4.8
* python-numpy 1.8.2

詳細
------
### 使い方 ###
    $ ./run.sh http://mjpg-streamer:9000/?action=stream

### entrance-monitor.py ###
------
コマンドライン引数を1つ取ります．
MJPG-Streamer のストリームが見られる URI を入力してください．

標準出力に3フレーム間の画像の類似度を出力し続けます．
類似度が 0.99 より小さくなれば jpg/ 以下にその時取得した画像を保存します．

ライセンス
----------
Copyright &copy; 2016 okabi
Distributed under the [MIT License][mit].

[MIT]: http://www.opensource.org/licenses/mit-license.php
