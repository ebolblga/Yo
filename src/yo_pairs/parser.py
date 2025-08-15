from typing import Dict


def parse_frequency_map(text: str) -> Dict[str, int]:
    freq = {}
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        parts = s.rsplit(None, 1)
        if len(parts) != 2:
            continue
        word, cnt = parts
        cnt = cnt.replace('\u00a0', '').replace(',', '')
        try:
            freq[word] = int(cnt)
        except ValueError:
            continue
    return freq
