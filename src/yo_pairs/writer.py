import itertools
import re
from pathlib import Path
from typing import Iterable, List, Tuple


def add_to_readme(
    results_path: str,
    readme_path: str = 'README.md',
    lines: int = 22,
    marker_start: str = '<!-- results table start -->',
    marker_end: str = '<!-- results table end -->',
    append_if_missing: bool = True,
) -> None:
    """
    Read up to `lines` from results_path and insert them into README.md
    between marker_start and marker_end. If the markers are not found and
    append_if_missing is True, append the block to the end of README.md.
    """

    results_file = Path(results_path)
    readme_file = Path(readme_path)

    if not results_file.exists():
        raise FileNotFoundError(f'{results_file} does not exist')

    with results_file.open('r', encoding='utf-8') as f:
        snippet_lines = list(itertools.islice(f, lines))

    snippet = ''.join(snippet_lines)
    if snippet and not snippet.endswith('\n'):
        snippet += '\n'

    new_block = f'{marker_start}\n{snippet}{marker_end}'

    readme_text = (
        readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''
    )

    # Regex to find existing block (non-greedy)
    pattern = re.compile(
        rf'{re.escape(marker_start)}.*?{re.escape(marker_end)}',
        flags=re.DOTALL,
    )

    if pattern.search(readme_text):
        updated = pattern.sub(new_block, readme_text)
    else:
        if append_if_missing:
            if readme_text and not readme_text.endswith('\n'):
                readme_text += '\n'
            updated = readme_text + new_block + '\n'
        else:
            raise RuntimeError(
                'Markers not found in README.md and append_if_missing is False'
            )

    readme_file.write_text(updated, encoding='utf-8')


def _fmt_lemma_block(lemma: str, derived_forms: Iterable[str]) -> str:
    """
    Format one lemma and its derived forms as:
    lemma: form1; form2; form3
    If derived_forms only contains lemma itself, just return lemma.
    """
    forms = list(dict.fromkeys(derived_forms))  # dedupe preserving order
    if not forms:
        return lemma
    # omit duplicate lemma inside derived forms if it's identical
    derived = ', '.join(forms)
    return f'{lemma}: {derived}'


def write_output(
    rows: Iterable[
        Tuple[
            str,
            str,
            int,
            List[Tuple[str, List[str]]],
            List[Tuple[str, List[str]]],
        ]
    ],
    filename: str,
) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(
            "| Index | Word with 'ё' | Lemma and derived forms | Word with 'е' | Lemma and derived forms | Combined Frequency |\n"
        )
        f.write('|-|-|-|-|-|-|\n')
        for idx, (yo, e, freq, yo_lemmas, e_lemmas) in enumerate(
            rows, start=1
        ):
            # format lemmas: produce semicolon-separated blocks "lemma: form1; form2"
            def format_blocks(blocks: List[Tuple[str, List[str]]]) -> str:
                if not blocks:
                    return ''
                pieces = []
                for lemma, forms in blocks:
                    pieces.append(_fmt_lemma_block(lemma, forms))
                return ' / '.join(pieces)

            yo_block = format_blocks(yo_lemmas)
            e_block = format_blocks(e_lemmas)
            f.write(
                f'| {idx} | {yo} | {yo_block} | {e} | {e_block} | {freq} |\n'
            )

    add_to_readme(results_path=filename, readme_path='README.md', lines=5)
    add_to_readme(results_path=filename, readme_path='README.en.md', lines=5)
