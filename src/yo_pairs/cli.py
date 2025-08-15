import os
import sys
from os import getenv
from typing import Dict, List, Optional, Set, Tuple

from dotenv import load_dotenv

from .downloader import ensure_local_copy, read_local_text
from .pair_finder import find_ё_pairs
from .parser import parse_frequency_map
from .validator import load_zaliznjak_forms
from .writer import write_output

load_dotenv('.env')

RAW_FREQ_URL = getenv(
    'RAW_FREQ_URL',
    'https://raw.githubusercontent.com/Baksalyar/mc.hertzbeat.ru-Frequency-Dictionaries/master/mc.hertzbeat.ru_frequency_dict.txt',
)
RAW_FREQ_PATH = getenv(
    'RAW_FREQ_PATH', 'raw/mc.hertzbeat.ru_frequency_dict.txt'
)

VALIDATOR_URL = getenv(
    'VALIDATOR_URL',
    'https://raw.githubusercontent.com/ebolblga/car-p18s/master/public/Library/russianUTF-8.txt',
)
VALIDATOR_PATH = getenv('VALIDATOR_PATH', 'raw/russianUTF-8.txt')

OUT_PATH_DEFAULT = getenv('OUT_PATH_DEFAULT', 'output/result.md')


def _get_lemma_blocks_for_word(
    word: str,
    form_to_lemmas: Dict[str, Set[str]],
    lemma_to_forms: Dict[str, Set[str]],
) -> List[Tuple[str, List[str]]]:
    """
    Return list of (lemma, [forms...]) for this word if present in form_to_lemmas.
    - word: raw token (may contain 'ё' or case)
    - keys in maps are casefolded and stress marks are removed
    """
    key = word.replace("'", '').replace('`', '').casefold()
    if key not in form_to_lemmas:
        return []  # not present
    lemmas = sorted(
        form_to_lemmas[key]
    )  # sorted set of lemma strings (cleaned)
    blocks = []
    for lemma in lemmas:
        lemma_key = lemma.casefold()
        derived = sorted(lemma_to_forms.get(lemma_key, {lemma}))
        blocks.append((lemma, derived))
    return blocks


def main(argv: Optional[list[str]] = None) -> None:
    argv = argv or sys.argv[1:]
    import argparse

    ap = argparse.ArgumentParser(
        description='Find ё->е pairs and expand with Zaliznjak lemmas/forms'
    )
    ap.add_argument('--output', '-o', default=OUT_PATH_DEFAULT)
    ap.add_argument(
        '--validate',
        choices=('none', 'first', 'second', 'both'),
        default='both',
        help='which words to require presence in zaliznjak_forms.txt (default: both)',
    )
    ap.add_argument(
        '--no-download',
        action='store_true',
        help='fail if required raw files are missing instead of downloading',
    )
    args = ap.parse_args(argv)

    # ensure frequency file
    try:
        if args.no_download and not os.path.exists(RAW_FREQ_PATH):
            raise RuntimeError(
                f'{RAW_FREQ_PATH} not found and --no-download set'
            )
        ensure_local_copy(RAW_FREQ_PATH, RAW_FREQ_URL)
    except Exception as e:
        print('Error ensuring frequency file:', e, file=sys.stderr)
        sys.exit(1)

    # ensure zaliznjak forms file
    try:
        if args.no_download and not os.path.exists(VALIDATOR_PATH):
            raise RuntimeError(
                f'{VALIDATOR_PATH} not found and --no-download set'
            )
        ensure_local_copy(VALIDATOR_PATH, VALIDATOR_URL)
    except Exception as e:
        print('Error ensuring zaliznjak forms file:', e, file=sys.stderr)
        sys.exit(1)

    # read sources
    try:
        freq_text = read_local_text(RAW_FREQ_PATH)
    except Exception as e:
        print('Failed to read frequency file:', e, file=sys.stderr)
        sys.exit(1)

    try:
        # use utf-8-sig to remove BOM if present
        with open(VALIDATOR_PATH, 'r', encoding='utf-8-sig') as fh:
            zal_text = fh.read()
    except Exception as e:
        print('Failed to read zaliznjak forms file:', e, file=sys.stderr)
        sys.exit(1)

    freq_map = parse_frequency_map(freq_text)
    if not freq_map:
        print('No valid entries parsed from frequency source', file=sys.stderr)
        sys.exit(1)

    # find base pairs (yo_word, e_word, combined_freq)
    pairs = find_ё_pairs(freq_map)

    # load zaliznjak mapping
    form_to_lemmas, lemma_to_forms = load_zaliznjak_forms(zal_text)

    # build final rows while applying validation mode
    final_rows = []
    for yo, e, freq in pairs:
        yo_key = yo.replace("'", '').replace('`', '').casefold()
        e_key = e.replace("'", '').replace('`', '').casefold()

        # validation checks
        if args.validate in ('first', 'both'):
            if yo_key not in form_to_lemmas:
                continue
        if args.validate in ('second', 'both'):
            if e_key not in form_to_lemmas:
                continue
        # get lemma blocks (may be empty if word absent and validate=none or optional)
        yo_blocks = _get_lemma_blocks_for_word(
            yo, form_to_lemmas, lemma_to_forms
        )
        e_blocks = _get_lemma_blocks_for_word(
            e, form_to_lemmas, lemma_to_forms
        )

        final_rows.append((yo, e, freq, yo_blocks, e_blocks))

    # final sort by combined frequency desc
    final_rows.sort(key=lambda t: t[2], reverse=True)

    if not final_rows:
        print('No pairs after validation/filtering.')
        return

    write_output(final_rows, args.output)
    print(f'Wrote {len(final_rows)} pairs to {args.output}')
