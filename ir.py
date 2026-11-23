"""bto_advanced_USBIR_cmd を呼び出して赤外線を送受信する。"""
import json
import re
import subprocess
import threading
from pathlib import Path

BASE = Path(__file__).resolve().parent
CMD = BASE / "vendor/bto_advanced_USBIR_cmd-1.0.1/bto_advanced_USBIR_cmd"
CODES = BASE / "codes"
BUTTONS = BASE / "buttons.json"
DATA_RE = re.compile(r"^0x[0-9a-f]{2}(,0x[0-9a-f]{2})*$")

# デバイスは同時に1つの操作しか受け付けないので、プロセス内で直列化する
_lock = threading.Lock()


class IRError(Exception):
    pass


def run(*args: str) -> str:
    with _lock:
        r = subprocess.run([str(CMD), *args], capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        raise IRError(f"exit {r.returncode}: {r.stderr.strip()}")
    return r.stdout.strip()


def load_buttons() -> list[dict]:
    return json.loads(BUTTONS.read_text(encoding="utf-8"))


def code_path(button_id: str) -> Path:
    ids = {b["id"] for b in load_buttons()}
    if button_id not in ids:
        raise IRError(f"unknown button: {button_id}")
    return CODES / f"{button_id}.txt"


def send(button_id: str) -> None:
    path = code_path(button_id)
    if not path.exists():
        raise IRError(f"not learned: {button_id}")
    run("-d", path.read_text().strip())


def start_receive() -> None:
    run("-r")


def stop_and_get() -> str:
    run("-s")
    data = run("-g")
    if not DATA_RE.match(data):
        raise IRError("受信データがない。もう一度やり直すこと")
    return data
