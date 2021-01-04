# 手順
* 出力されたtarファイルをダウンロードしてくる
* `tar xf takeout-xxx-001.tar`で解凍する
    * 複数のtarがある場合も、Takeoutディレクトリに追記されるので、全部解凍する
* `python flatten.py`
* `aws s3 sync result s3://twinrabbits-photo-backup/backup/`
