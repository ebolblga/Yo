import itertools
import re
from pathlib import Path
from typing import List, Tuple


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


def write_output(pairs: List[Tuple[str, str, int]], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(
            "| Индекс | Слово с 'ё' | Слово с 'е' "
            '| Комбинированная частота |\n'
        )
        f.write('|-|-|-|-|\n')
        for idx, (yo, e, freq) in enumerate(pairs, 1):
            f.write(f'| {idx} | {yo} | {e} | {freq} |\n')

    add_to_readme(results_path=filename, readme_path='README.md', lines=22)
    add_to_readme(results_path=filename, readme_path='README.en.md', lines=22)
