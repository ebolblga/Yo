import sys
from typing import List, Optional, Set, Tuple

from .downloader import ensure_local_copy, read_local_text
from .pair_finder import find_ё_pairs
from .parser import parse_frequency_map
from .validator import is_word_valid, load_wordset_from_text
from .writer import write_output

RAW_FREQ_URL = 'https://raw.githubusercontent.com/Baksalyar/mc.hertzbeat.ru-Frequency-Dictionaries/master/mc.hertzbeat.ru_frequency_dict.txt'
RAW_FREQ_PATH = 'raw/mc.hertzbeat.ru_frequency_dict.txt'

VALIDATOR_URL = 'https://raw.githubusercontent.com/ebolblga/car-p18s/master/public/Library/russianUTF-8.txt'
VALIDATOR_PATH = 'raw/russianUTF-8.txt'

OUT_PATH_DEFAULT = 'output/result.md'


def filter_pairs(
    pairs: List[Tuple[str, str, int]], validator_set: Set[str], mode: str
) -> List[Tuple[str, str, int]]:
    """
    mode: one of 'none', 'first', 'second', 'both'
    """
    if mode == 'none':
        return pairs

    filtered = []
    for yo, e, freq in pairs:
        ok_first = True
        ok_second = True
        if mode in ('first', 'both'):
            ok_first = is_word_valid(yo, validator_set)
        if mode in ('second', 'both'):
            ok_second = is_word_valid(e, validator_set)
        if ok_first and ok_second:
            filtered.append((yo, e, freq))
    return filtered


def main(argv: Optional[list[str]] = None) -> None:
    argv = argv or sys.argv[1:]
    import argparse

    ap = argparse.ArgumentParser(
        description='Find ё -> е word pairs and filter with validator list'
    )
    ap.add_argument(
        '--output',
        '-o',
        default=OUT_PATH_DEFAULT,
        help='output filename (markdown table)',
    )
    ap.add_argument(
        '--validate',
        choices=('none', 'first', 'second', 'both'),
        default='both',
        help=(
            'which words to validate against russianUTF-8.txt (default: both)'
        ),
    )
    ap.add_argument(
        '--no-download',
        action='store_true',
        help='fail if required raw files are missing instead of downloading',
    )
    args = ap.parse_args(argv)

    # Ensure frequency file
    try:
        if args.no_download and not __import__('os').path.exists(
            RAW_FREQ_PATH
        ):
            raise RuntimeError(
                f'{RAW_FREQ_PATH} not found and --no-download set'
            )
        ensure_local_copy(RAW_FREQ_PATH, RAW_FREQ_URL)
    except Exception as e:
        print('Error ensuring frequency file:', e, file=sys.stderr)
        sys.exit(1)

    # Ensure validator file
    try:
        if args.no_download and not __import__('os').path.exists(
            VALIDATOR_PATH
        ):
            raise RuntimeError(
                f'{VALIDATOR_PATH} not found and --no-download set'
            )
        ensure_local_copy(VALIDATOR_PATH, VALIDATOR_URL)
    except Exception as e:
        print('Error ensuring validator file:', e, file=sys.stderr)
        sys.exit(1)

    # Read
    freq_text = read_local_text(RAW_FREQ_PATH)
    validator_text = read_local_text(VALIDATOR_PATH)

    freq_map = parse_frequency_map(freq_text)
    if not freq_map:
        print('No valid entries parsed from frequency source', file=sys.stderr)
        sys.exit(1)

    pairs = find_ё_pairs(freq_map)

    validator_set = load_wordset_from_text(validator_text)

    pairs = filter_pairs(pairs, validator_set, args.validate)

    pairs.sort(key=lambda t: t[2], reverse=True)

    if not pairs:
        print('No pairs after validation/filtering.')
    else:
        write_output(pairs, args.output)
        print(f'Wrote {len(pairs)} pairs to {args.output}')
