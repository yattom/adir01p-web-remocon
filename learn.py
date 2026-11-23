"""リモコンのボタンを1つ学習して codes/<id>.txt に保存する。

使い方: uv run learn.py <button_id>
"""
import sys

import ir


def main() -> None:
    if len(sys.argv) != 2:
        ids = ", ".join(b["id"] for b in ir.load_buttons())
        sys.exit(f"使い方: uv run learn.py <button_id>\nbutton_id: {ids}")
    path = ir.code_path(sys.argv[1])

    ir.start_receive()
    input("受信中。リモコンを本体に向けてボタンを1回押し、Enter を押す: ")
    data = ir.stop_and_get()
    path.write_text(data + "\n")
    print(f"保存した: {path} ({data.count(',') + 1} bytes)")

    if input("送信して確認する? [y/N]: ").strip().lower() == "y":
        ir.send(sys.argv[1])
        print("送信した")


if __name__ == "__main__":
    main()
