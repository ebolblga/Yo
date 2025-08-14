import sys

from .downloader import ensure_local_copy, read_local_text
from .pair_finder import find_ё_pairs
from .parser import parse_frequency_map
from .writer import write_output

RAW_URL = 'https://raw.githubusercontent.com/Baksalyar/mc.hertzbeat.ru-Frequency-Dictionaries/master/mc.hertzbeat.ru_frequency_dict.txt'
RAW_PATH = 'raw/mc.hertzbeat.ru_frequency_dict.txt'
OUT_PATH = 'output/result.md'


def main() -> None:
    try:
        ensure_local_copy(RAW_PATH, RAW_URL)
        text = read_local_text(RAW_PATH)
    except Exception as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(1)

    freq = parse_frequency_map(text)
    pairs = find_ё_pairs(freq)
    if not pairs:
        print('No ё/e pairs found')
        return
    write_output(pairs, OUT_PATH)
    print(f'Wrote {len(pairs)} pairs to {OUT_PATH}')


if __name__ == '__main__':
    main()
