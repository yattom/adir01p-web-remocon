# ADIR01P ケース設計 引き継ぎメモ

## 目的
Bit Trade One「USB赤外線リモコンアドバンス」ADIR01P のケースを 3D プリンタで作る。
- ホコリよけ
- 基板上で常時点滅している赤色 LED を隠す(ソフトウェアからは消灯できないことを確認済み)
- 赤外線の送受信と USB 接続は妨げない

設計は OpenSCAD で行い、STL を出力してスライサーに渡す想定。

## 基板の寸法(メーカー寸法図 v1.13 より)
- 基板外形: 67 × 27 mm(角は面取りあり)。厚さは未確認(一般的には 1.6 mm)
- 取り付け穴: 直径 2.2 mm(M2 用)× 3
  - 左下角から X=13.5, Y=13.5
  - 右端から 3 mm、下端から Y=8.5 と Y=18.5(2 つの間隔 10 mm)
- USB mini-B: 左端、縦方向の中央付近
- 赤外線 LED 3 基(LD1〜LD3、5 mm 砲弾型): 右寄りに縦一列(下から LD1, LD2, LD3)
- 赤外線受光部(RCV、3 本足): LD3 の左上あたり、上端寄り
- 表示用 LED 2 個(LED1, LED2、チップ LED): どちらもマイコン制御
  - LED1: 中央上の IC1 の左上あたり
  - LED2: 右側の Q1 の左あたり
  - メーカー FAQ によると緑の LED は赤外線検出時に点滅する。赤の LED は常時点滅

資料(メーカー GitHub):
- 寸法図: https://github.com/bit-trade-one/ADIR01P-USB_IR_Remote_Controller_Advance/blob/master/Dimensions/ir_pro_v1-13_dimensions.pdf
- 回路図: https://github.com/bit-trade-one/ADIR01P-USB_IR_Remote_Controller_Advance/blob/master/Schematics/ir_pro_v1-13_schematics.pdf
- FAQ: https://github.com/bit-trade-one/ADIR01P-USB_IR_Remote_Controller_Advance/blob/master/FAQ.md

## 開口部の方針
- 開ける: 赤外線 LED 3 基の前、受光部の前、USB 差し込み口
- ふさぐ: 赤色の点滅 LED の上
- それ以外もできるだけふさぐ(ホコリ対策)

## 未確定事項(実物を見て決める)
1. 赤外線 LED と USB コネクタの基板からの高さ(ノギスで実測)
2. 赤外線 LED が基板に垂直に立っているか、横に倒れているか → 開口を上面か側面か
3. 点滅している赤色 LED が LED1 と LED2 のどちらか
4. 設置の向き(テレビ側に向ける面、USB ケーブルの出す方向)
5. プリンタ機種・材料・色(色によって赤外線を通しにくいので開口の大きさに関係)
6. 固定方法(M2 ねじ / はめ込み)

## 背景(参考)
- ラズパイ 4 に USB 接続し、Flask の Web アプリからスマホでテレビ(東芝)とレコーダー(パナソニック DIGA)を操作している
- ケースを付けたあとも、学習(受信)と送信ができることを確認する
