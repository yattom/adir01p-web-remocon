#!/bin/sh
# sudo が必要なシステム設定をまとめて行う。実行: sudo sh setup/setup_system.sh
set -eu
cd "$(dirname "$0")"

apt-get install -y libusb-1.0-0-dev

install -m 0644 99-adir01p.rules /etc/udev/rules.d/99-adir01p.rules
udevadm control --reload
udevadm trigger --subsystem-match=usb --attr-match=idVendor=22ea

install -m 0644 remocon.service /etc/systemd/system/remocon.service
systemctl daemon-reload
systemctl enable --now remocon.service

echo "完了。デバイスの権限:"
ls -l /dev/bus/usb/*/* | grep plugdev || echo "plugdev のデバイスが見つからない"
