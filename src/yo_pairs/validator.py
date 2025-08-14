from typing import Set


def load_wordset_from_text(text: str) -> Set[str]:
    """
    Build a set of words from the validator text file.
    Uses casefold() for case-insensitive membership checks.
    """
    s = set()
    for ln in text.splitlines():
        w = ln.strip()
        if not w:
            continue
        s.add(w.casefold())
    return s


def is_word_valid(word: str, wordset: Set[str]) -> bool:
    """
    Case-insensitive check. Returns True if word.casefold() is in wordset.
    """
    return word.casefold() in wordset
