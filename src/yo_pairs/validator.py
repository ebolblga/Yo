from typing import Dict, Set, Tuple


def _clean_token(s: str) -> str:
    """Remove stress marks and surrounding whitespace."""
    return s.replace("'", '').replace('`', '').strip()


def load_zaliznjak_forms(
    text: str,
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Parse zaliznjak forms file text and return:
      (form_to_lemmas, lemma_to_forms)

    - Handles UTF-8 BOM if caller used 'utf-8-sig' when reading.
    - Lines expected like: form, lemma
      There may be multiple lemmas separated by commas.
    - Both maps use casefold() keys for matching.
    """
    form_to_lemmas: Dict[str, Set[str]] = {}
    lemma_to_forms: Dict[str, Set[str]] = {}

    for raw_ln in text.splitlines():
        ln = raw_ln.strip()
        if not ln:
            continue
        # split into form and rest (lemmas)
        parts = ln.split(',', 1)
        if not parts:
            continue
        form_raw = parts[0].strip()
        rest = parts[1].strip() if len(parts) > 1 else ''
        form = _clean_token(form_raw)
        if not form:
            continue

        # parse lemmas (may be comma-separated)
        lemmas = []
        if rest:
            # split by comma; sometimes semicolon or other separators appear
            # prioritize comma split
            if ',' in rest:
                for p in rest.split(','):
                    p = p.strip()
                    if p:
                        lemmas.append(_clean_token(p))
            elif ';' in rest:
                for p in rest.split(';'):
                    p = p.strip()
                    if p:
                        lemmas.append(_clean_token(p))
            else:
                lemmas.append(_clean_token(rest))

        # if no lemma provided, treat form as its own lemma
        if not lemmas:
            lemmas = [form]

        form_key = form.casefold()
        if form_key not in form_to_lemmas:
            form_to_lemmas[form_key] = set()
        for lemma in lemmas:
            if not lemma:
                continue
            lemma_key = lemma.casefold()
            form_to_lemmas[form_key].add(lemma)

            if lemma_key not in lemma_to_forms:
                lemma_to_forms[lemma_key] = set()
            lemma_to_forms[lemma_key].add(form)

    return form_to_lemmas, lemma_to_forms
