#!/bin/sh
# Wi-Fi 省電力をオフにする。実行: sudo sh setup/wifi_powersave_off.sh
set -eu
cd "$(dirname "$0")"
# 再起動後も有効にする設定 (NetworkManager が接続時に適用する)
install -m 0644 wifi-powersave-off.conf /etc/NetworkManager/conf.d/wifi-powersave-off.conf
# 今すぐ反映する (接続は切れない)
iw dev wlan0 set power_save off
iw dev wlan0 get power_save
