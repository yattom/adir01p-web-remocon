# remote_remocon

Raspberry Pi に USB 赤外線リモコン（Bit Trade One ADIR01P）をつなぎ、スマホのブラウザからテレビやレコーダーを操作する Web リモコン。

- リモコンの信号を学習して保存し、Web 画面のボタンから送信する
- 同じ Wi-Fi 内のスマホ（Android / iPhone）から http で使う。ホーム画面に追加できる
- 画面のボタン配置と色は、パナソニック DIGA のリモコンに合わせている

## 動作確認環境

| 項目 | 内容 |
|---|---|
| 本体 | Raspberry Pi 4 Model B |
| OS | Debian GNU/Linux 13 (trixie) aarch64（Raspberry Pi OS） |
| 赤外線デバイス | Bit Trade One USB赤外線リモコンアドバンス ADIR01P（USB ID `22ea:003a`、ファームウェア 1.3.4） |
| 制御ツール | bto_advanced_USBIR_cmd 1.0.1（`vendor/` に同梱、libusb-1.0 を使用） |
| Python | 3.13 |
| パッケージ管理 | uv 0.13.9 |
| Web フレームワーク | Flask 3.1.3（依存関係は `uv.lock` で固定） |
| ネットワーク | NetworkManager（Wi-Fi 省電力の設定に使用） |
| 操作対象 | 東芝のテレビ（NEC フォーマット）、パナソニック DIGA（家電協フォーマット） |

ADIR01P はメーカーとしては Windows のみの対応で、Linux での動作はメーカーの保証外。

## 構成

```
スマホのブラウザ
  │ http://<ホスト名>.local:8000
  ▼
app.py（Flask）── ir.py ── bto_advanced_USBIR_cmd ── ADIR01P ──(赤外線)── テレビ / レコーダー
```

- `app.py` … Web 画面と送信 API（`POST /send/<button_id>`）
- `ir.py` … 制御ツールの呼び出し。同時実行はロックで1つずつに制限する
- `learn.py` … ボタンを1つ学習するコマンド
- `buttons.json` … ボタンの ID と表示名
- `codes/<button_id>.txt` … 学習した信号データ
- `templates/index.html` … 画面
- `static/` … ホーム画面用アイコン（`icon-source.html` を headless chromium で PNG にしたもの）
- `setup/` … udev ルール、systemd ユニット、セットアップ用スクリプト
- `vendor/bto_advanced_USBIR_cmd-1.0.1/` … 制御ツールのソース（メーカー配布の zip を展開したもの）

## セットアップ

### 1. 取得と Python 環境

```
git clone <このリポジトリ> ~/remote_remocon
cd ~/remote_remocon
uv sync
```

### 2. systemd ユニットの書き換え

`setup/remocon.service` の `User` と各パスを、自分の環境に合わせて書き換える。

### 3. システム設定（sudo が必要）

```
sudo sh setup/setup_system.sh
```

次のことを行う。

- `libusb-1.0-0-dev` をインストールする
- udev ルールを置き、ADIR01P を `plugdev` グループから使えるようにする（実行するユーザーは `plugdev` に入っている必要がある）
- systemd にサービスを登録して起動する（ポート 8000）

メーカー配布の Makefile の `make install` は setuid root でインストールするが、ここでは使わない。udev ルールで権限を与え、ツールは `vendor/` 内でビルドしたものを直接呼び出す。

### 4. 制御ツールのビルド

```
make -C vendor/bto_advanced_USBIR_cmd-1.0.1
./vendor/bto_advanced_USBIR_cmd-1.0.1/bto_advanced_USBIR_cmd --firmversion
```

`Firmware version ...` と表示されれば、sudo なしでデバイスと通信できている。

### 5. Wi-Fi 省電力をオフにする（任意）

Raspberry Pi の Wi-Fi は省電力が有効だと、スマホからの操作に 0.1〜0.3 秒ほど遅れが出ることがある。

```
sudo sh setup/wifi_powersave_off.sh
```

## ボタンの学習

```
uv run learn.py <button_id>
```

1. 「受信中」と表示されたら、リモコンを ADIR01P に近づけて向け、ボタンを1回押して Enter を押す
2. `codes/<button_id>.txt` に保存される
3. `y` を押すとその場で送信して確認できる

「受信データがない」と表示されたら、もう一度実行する。

ボタンを増やすときは、`buttons.json` に追加し、`templates/index.html` に配置を書く。

### 学習のときの注意

- リモコンのボタンを押すと、同じ信号が2〜3回、あるいはリピート信号が続けて記録されることがある。テレビの音量などは、これで2段階動くことがある。その場合は、信号を最初の1回分だけ残すように `codes/<button_id>.txt` を編集する
- 周りの光などの雑音が信号の前に記録され、送信しても機器が反応しないことがある。その場合は学習し直す
- 信号データは、4バイトで1組（点灯時間・消灯時間を2バイトずつ）の並び

## 使い方

スマホのブラウザで `http://<ホスト名>.local:8000` を開く。名前で開けない場合は IP アドレスを使う（ルーターで IP を固定しておくとよい）。

- ボタンを押すと、送信に成功したら枠が緑、失敗したら赤になる
- 学習していないボタンは灰色で押せない
- ブラウザのメニューから「ホーム画面に追加」できる。http のため、Android ではブラウザのタブとして開く

## 注意

- 認証はない。同じネットワークにいる人は誰でも操作できる。家庭内の Wi-Fi で使う前提で、インターネットには公開しないこと（外から使う場合は VPN を使う）
- 送信しても機器の状態は分からない（電源がオンかオフかなど）
- ADIR01P の基板上の赤色 LED は、つないでいる間ずっと点滅する。ソフトウェアからは消せない

## ライセンス

MIT License（`LICENSE` を参照）。

ただし `vendor/bto_advanced_USBIR_cmd-1.0.1/` は対象外で、Assembly Desk License (ADL)、(C) Bit Trade One, LTD. に従う。一部は MIT License (Copyright (c) 2013 Kazunori Kojima)。詳細は同ディレクトリの `License_ADL.txt`、`License_MIT.txt`、`README.txt` を参照。

## 参考

- [ADIR01P 製品ページ](https://bit-trade-one.co.jp/product/module/adir01p/)
- [ADIR01P メーカー GitHub（寸法図・回路図・FAQ）](https://github.com/bit-trade-one/ADIR01P-USB_IR_Remote_Controller_Advance)
- [ラズパイで ADIR01P を使う（hymd3a）](https://hymd3a.hatenablog.com/entry/2021/05/11/193506)
- [ラズパイで ADIR01P を使う（ponkichi）](https://ponkichi.blog/smart-remocon/)
