import os

import requests


def ensure_local_copy(
    local_path: str, remote_url: str, timeout: int = 30
) -> None:
    if os.path.exists(local_path):
        return
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    r = requests.get(remote_url, timeout=timeout)
    r.raise_for_status()
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(r.text)


def read_local_text(local_path: str) -> str:
    with open(local_path, 'r', encoding='utf-8') as f:
        return f.read()
