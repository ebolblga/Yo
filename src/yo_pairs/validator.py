from typing import Dict, Set, Tuple


def _clean_token(s: str) -> str:
    """Remove stress marks and surrounding whitespace for keys."""
    return s.replace("'", '').replace('`', '').strip()


def _prettify_stress(s: str) -> str:
    """
    Convert stress markers (single-quote ' and backtick `) into a combining acute
    accent (U+0301) attached to the previous character.

    Example: "аба'" -> "аба́"
    The returned string does NOT contain the original marker characters.
    """
    result: list[str] = []
    for ch in s:
        if ch in ("'", '`'):
            # Attach combining acute to previous character if available
            if result:
                result[-1] = result[-1] + '\u0301'
            # If there's no previous character, skip the marker
            continue
        result.append(ch)
    return ''.join(result)


def load_validation_file(
    text: str,
) -> Tuple[
    Dict[str, Set[str]], Dict[str, Set[str]], Dict[str, str], Dict[str, str]
]:
    """
    Parse zaliznjak forms text and return:
        (form_to_lemmas, lemma_to_forms, form_display_map, lemma_display_map)

    - form_to_lemmas: form_key -> set(lemma_key)
    - lemma_to_forms: lemma_key -> set(form_key)
    - form_display_map: form_key -> pretty_display_string (with combining accent)
    - lemma_display_map: lemma_key -> pretty_display_string

    Keys are created by removing stress markers and casefolding for robust lookup.
    Display strings preserve stress and convert markers to combining accents.
    """
    form_to_lemmas: Dict[str, Set[str]] = {}
    lemma_to_forms: Dict[str, Set[str]] = {}
    form_display_map: Dict[str, str] = {}
    lemma_display_map: Dict[str, str] = {}

    for raw_ln in text.splitlines():
        ln = raw_ln.strip()
        if not ln:
            continue
        parts = ln.split(',', 1)
        if not parts:
            continue
        form_raw = parts[0].strip()
        rest = parts[1].strip() if len(parts) > 1 else ''

        # Build clean key for the form
        form_clean = _clean_token(form_raw)
        if not form_clean:
            continue
        form_key = form_clean.casefold()

        # Build pretty/display version for the form (convert stress markers -> combining accents)
        form_display = _prettify_stress(form_raw).strip()
        # If prettified string is empty for some reason, fall back to cleaned form
        if not form_display:
            form_display = form_clean

        # Parse lemmas
        lemmas_raw: list[str] = []
        if rest:
            if ',' in rest:
                for p in rest.split(','):
                    p = p.strip()
                    if p:
                        lemmas_raw.append(p)
            elif ';' in rest:
                for p in rest.split(';'):
                    p = p.strip()
                    if p:
                        lemmas_raw.append(p)
            else:
                lemmas_raw.append(rest.strip())
        # If no lemma present, treat form as its own lemma
        if not lemmas_raw:
            lemmas_raw = [form_raw]

        # Ensure maps have entries
        if form_key not in form_to_lemmas:
            form_to_lemmas[form_key] = set()
        # Save display
        form_display_map[form_key] = form_display

        for lemma_raw in lemmas_raw:
            lemma_clean = _clean_token(lemma_raw)
            if not lemma_clean:
                continue
            lemma_key = lemma_clean.casefold()
            # Pretty lemma for display
            lemma_display = _prettify_stress(lemma_raw).strip() or lemma_clean
            lemma_display_map.setdefault(lemma_key, lemma_display)

            # Map relations
            form_to_lemmas[form_key].add(lemma_key)
            lemma_to_forms.setdefault(lemma_key, set()).add(form_key)

    return form_to_lemmas, lemma_to_forms, form_display_map, lemma_display_map
